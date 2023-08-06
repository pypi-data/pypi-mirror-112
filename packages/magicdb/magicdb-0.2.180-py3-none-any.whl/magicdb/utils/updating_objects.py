import typing as T
import magicdb
from magicdb import DELETE_FIELD, ArrayUnion, ArrayRemove


def make_update_obj_rec(
    original, new, current_path, update_d, fields_for_array_actions: T.Set[str]
):
    field_path = magicdb.db.conn.field_path

    # first get all the deletions of fields
    del_fields = original.keys() - new.keys()
    for field in del_fields:

        update_d[".".join([*current_path, field_path(field)])] = DELETE_FIELD

    # now get all the object and value changes
    for field, new_value in new.items():
        if field not in original:
            update_d[".".join([*current_path, field_path(field)])] = new_value
            continue
        original_value = original[field]
        if new_value == original_value:
            continue
        # this is the case where they are different...
        if type(new_value) != type(original_value) or not type(new_value) == dict:
            try:
                raw_path = ".".join([*current_path, field])
                if (
                    issubclass(type(new_value), list)
                    and raw_path in fields_for_array_actions
                ):
                    # try and array union or remove
                    # you want to preserve order tho
                    print(
                        f"here {new_value=}, {raw_path=}, {fields_for_array_actions=}"
                    )
                    if len(new_value) > len(original_value):
                        if new_value[: len(original_value)] == original_value:
                            appended_values = new_value[len(original_value) :]
                            update_d[
                                ".".join([*current_path, field_path(field)])
                            ] = ArrayUnion(values=appended_values)
                            continue
            except Exception as e:
                print("e in updating objects", e)

            update_d[".".join([*current_path, field_path(field)])] = new_value
            continue

        # now you know this is a dict and it's different
        make_update_obj_rec(
            original_value,
            new_value,
            [*current_path, field_path(field)],
            update_d,
            fields_for_array_actions=fields_for_array_actions,
        )


def make_update_obj(original, new, fields_for_array_actions: T.Set[str] = None):
    update_d = {}
    make_update_obj_rec(
        original=original,
        new=new,
        current_path=[],
        update_d=update_d,
        fields_for_array_actions=fields_for_array_actions or set(),
    )
    return update_d
