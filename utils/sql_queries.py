SELECT_OID = """
    SELECT oid
    FROM probability
    WHERE classifier_name = %(classifier_name)s
    AND class_name = ANY(%(classes)s)
    AND probability > %(probability)s
    LIMIT %(limit)s;
"""

VIEW_PROBABILITY = "SELECT probability FROM probability WHERE oid = ANY(%(oids)s)"


SELECT_OBJECT = """
    SELECT oid, meanra, meandec
    FROM object
    WHERE oid = ANY(%(oids)s)
"""

SELECT_DETECTION = """
    SELECT *
    FROM detection
    WHERE oid = ANY(%(oids)s)
"""

SELECT_NON_DETECTION = """
    SELECT *
    FROM non_detection
    WHERE oid = ANY(%(oids)s)
"""

FEATURES_QUERY = """
    SELECT DISTINCT version
    FROM feature
    WHERE oid = ANY(%(oids)s)
"""

FEATURES_VALUES_QUERY = """
    SELECT *
    FROM feature
    WHERE oid = ANY(%(oids)s)
    AND name = ANY(%(features)s)
"""
