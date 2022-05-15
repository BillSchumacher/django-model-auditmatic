"""
    function to generate sql trigger
"""


def generate_trigger(audit_name, table_name):
    """
        generates create trigger sql statement
    :param audit_name:
    :param table_name:
    :return: create trigger statement
    """
    return f"""
    CREATE OR REPLACE TRIGGER {audit_name}
        AFTER INSERT ON {table_name}
            FOR EACH ROW
        AFTER UPDATE ON {table_name}
            FOR EACH ROW
        AFTER DELETE ON {table_name}
            FOR EACH ROW
    EXECUTE PROCEDURE {audit_name}();
    """
