import os
import collections

from ..core import Core
from ..endpoint import SyncFolderItems, SyncFolderHierarchy, GetItem, ConvertId


class HierarchyProcessor:

    __FOLDER_HIERARCHY = []

    def __get_item(self, item_id, change_key=None):
        response = GetItem(item_id, change_key=change_key).run()
        if isinstance(response, list):
            if any(item in response for item in ConvertId.ID_FORMATS):
                convert_id_response = ConvertId(Core.credentials[0], item_id, id_type=response[0], convert_to=response[1]).run()
                get_item_response = GetItem(convert_id_response[0]).run()
                return get_item_response if get_item_response else None
        return GetItem(item_id, change_key=change_key).run()

    def __dict_merge(self, dct, merge_dct, add_keys=True):
        """ Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
        updating only top-level keys, dict_merge recurses down into dicts nested
        to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
        ``dct``.

        This version will return a copy of the dictionary and leave the original
        arguments untouched.

        The optional argument ``add_keys``, determines whether keys which are
        present in ``merge_dict`` but not ``dct`` should be included in the
        new dict.

        Args:
            dct (dict) onto which the merge is executed
            merge_dct (dict): dct merged into dct
            add_keys (bool): whether to add new keys

        Returns:
            dict: updated dict
        """
        dct = dct.copy()
        if not add_keys:
            merge_dct = {
                k: merge_dct[k]
                for k in set(dct).intersection(set(merge_dct))
            }
        for k, v in merge_dct.items():
            if (k in dct and isinstance(dct[k], dict)
                    and isinstance(merge_dct[k], collections.Mapping)):
                dct[k] = self.__dict_merge(dct[k], merge_dct[k], add_keys=add_keys)
            else:
                dct[k] = merge_dct[k]
        return dct

    def __get_children(self, parent, relations):
        children = (r[1] for r in relations if r[0] == parent)
        return {c: self.__get_children(c, relations) for c in children}

    def __sync_folder_items(self, tree):
        if isinstance(tree, dict):
            for key, val in tree.items():
                if key not in self.__FOLDER_HIERARCHY:
                    self.__FOLDER_HIERARCHY.append(key)
                if isinstance(val, dict):
                    self.__sync_folder_items(val)

    def __extract_item_id(self, data):
        for key,val in SyncFolderItems.FIELD_ACTION_TYPE_MAP.items():
            for item in val:
                if data.get(item.capitalize()):
                    return Core()._get_recursively(data.get(item.capitalize()).get('ItemId'), '@Id')
                elif data.get(item):
                    return Core()._get_recursively(data.get(item).get('item_id'), 'id')

    def __update_nested(self, in_dict, key):
        for k, v in in_dict.items():
            if key == k:
                details_list = []
                response = SyncFolderItems(k).run()
                for item in response:
                    if item and isinstance(item.get('create'), list):
                        for i in item.get('create'):
                            response = self.__extract_item_id(i)
                            if response:
                                for id in response:
                                    for sync_item in self.__get_item(id):
                                        details_list.append(
                                            self.__dict_merge(Core()._process_dict(i), Core()._process_dict(sync_item))
                                        )
                    elif item and isinstance(item.get('create'), dict):
                        response = self.__extract_item_id(item.get('create'))
                        if response:
                            for id in response:
                                for sync_item in self.__get_item(id):
                                    details_list.append(
                                        self.__dict_merge(Core()._process_dict(item), Core()._process_dict(sync_item))
                                    )
                if self.__folder_hierarchy_details.get(k):
                    in_dict[k].update(self.__folder_hierarchy_details[k])
                if details_list:
                    in_dict[k].update({'details': details_list})
            elif isinstance(v, dict):
                self.__update_nested(v, key)
            elif isinstance(v, list):
                for o in v:
                    if isinstance(o, dict):
                        self.__update_nested(o, key)
        return in_dict

    def sync(self):
        self.__folder_hierarchy_details = {}
        folder_hierarchy_list = []
        for item in SyncFolderHierarchy().run():
            for i in item.get('create'):
                for key,val in i.items():
                    if val.get('FolderId').get('@Id') not in self.__folder_hierarchy_details:
                        self.__folder_hierarchy_details[val.get('FolderId').get('@Id')] = Core()._process_dict(val)
                    folder_hierarchy_list.append((val.get('ParentFolderId').get('@Id'), val.get('FolderId').get('@Id')))
        parents, children = map(set, zip(*folder_hierarchy_list))
        folder_hierarchy_tree = {p: self.__get_children(p, folder_hierarchy_list) for p in (parents - children)}
        self.__sync_folder_items(folder_hierarchy_tree)
        for item in self.__FOLDER_HIERARCHY:
            self.__update_nested(folder_hierarchy_tree, item)
        return folder_hierarchy_tree
