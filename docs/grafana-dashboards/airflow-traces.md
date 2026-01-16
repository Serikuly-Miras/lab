{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": {
          "type": "grafana",
          "uid": "-- Grafana --"
        },
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 1)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 0,
  "id": 0,
  "links": [],
  "panels": [
    {
      "collapsed": false,
      "gridPos": {
        "h": 1,
        "w": 24,
        "x": 0,
        "y": 0
      },
      "id": 4,
      "panels": [],
      "title": "Traces overview",
      "type": "row"
    },
    {
      "datasource": {
        "type": "tempo",
        "uid": "${tempo_db}"
      },
      "fieldConfig": {
        "defaults": {
          "custom": {
            "align": "left",
            "cellOptions": {
              "type": "auto"
            },
            "filterable": true,
            "footer": {
              "reducers": []
            },
            "inspect": false,
            "wrapText": false
          },
          "links": [
            {
              "title": "Trace Link",
              "url": "/d/90e703ae-c528-46cc-963f-c8d60a139fdb/airflow-tracing?orgId=1&var-trace_id=${__data.fields[\"traceID\"]}"
            }
          ],
          "mappings": [],
          "thresholds": {
            "mode": "absolute",
            "steps": [
              {
                "color": "green",
                "value": 0
              }
            ]
          },
          "unit": "s"
        },
        "overrides": [
          {
            "matcher": {
              "id": "byName",
              "options": "Trace ID"
            },
            "properties": [
              {
                "id": "custom.width",
                "value": 104
              }
            ]
          },
          {
            "matcher": {
              "id": "byName",
              "options": "Start time"
            },
            "properties": [
              {
                "id": "custom.width",
                "value": 192
              }
            ]
          },
          {
            "matcher": {
              "id": "byName",
              "options": "Service"
            },
            "properties": [
              {
                "id": "custom.width",
                "value": 89
              }
            ]
          }
        ]
      },
      "gridPos": {
        "h": 15,
        "w": 24,
        "x": 0,
        "y": 1
      },
      "id": 1,
      "options": {
        "cellHeight": "sm",
        "enablePagination": true,
        "showHeader": true,
        "sortBy": [
          {
            "desc": true,
            "displayName": "Duration"
          }
        ]
      },
      "pluginVersion": "12.3.0",
      "targets": [
        {
          "datasource": {
            "type": "tempo",
            "uid": "${tempo_db}"
          },
          "filters": [
            {
              "id": "7ff760e1",
              "operator": "=",
              "scope": "span"
            },
            {
              "id": "service-name",
              "isCustomValue": false,
              "operator": "=",
              "scope": "resource",
              "tag": "service.name",
              "value": [
                "Airflow"
              ],
              "valueType": "string"
            }
          ],
          "limit": 20,
          "metricsQueryType": "range",
          "query": "{resource.service.name=\"Airflow\" && rootName=~\"$dag_id\"}",
          "queryType": "traceql",
          "refId": "A",
          "serviceMapUseNativeHistograms": false,
          "tableType": "traces"
        }
      ],
      "title": "Dag run traces",
      "type": "table"
    },
    {
      "datasource": {
        "type": "tempo",
        "uid": "${tempo_db}"
      },
      "fieldConfig": {
        "defaults": {},
        "overrides": []
      },
      "gridPos": {
        "h": 46,
        "w": 24,
        "x": 0,
        "y": 16
      },
      "id": 2,
      "options": {
        "spanFilters": {
          "criticalPathOnly": false,
          "matchesOnly": false,
          "serviceNameOperator": "=",
          "spanNameOperator": "=",
          "tags": [
            {
              "id": "807da799-85f",
              "operator": "="
            }
          ]
        }
      },
      "pluginVersion": "12.3.0",
      "targets": [
        {
          "datasource": {
            "type": "tempo",
            "uid": "${tempo_db}"
          },
          "filters": [
            {
              "id": "ebba848c",
              "isCustomValue": false,
              "operator": "=",
              "scope": "span",
              "tag": "airflow.dag_run.dag_id",
              "value": [
                "$dag_id"
              ]
            },
            {
              "id": "service-name",
              "isCustomValue": false,
              "operator": "=",
              "scope": "resource",
              "tag": "service.name",
              "value": [
                "Airflow"
              ],
              "valueType": "string"
            }
          ],
          "limit": 20,
          "metricsQueryType": "range",
          "query": "${trace_id}",
          "queryType": "traceql",
          "refId": "A",
          "serviceMapUseNativeHistograms": false,
          "tableType": "traces"
        }
      ],
      "title": "Trace viz",
      "type": "traces"
    }
  ],
  "preload": false,
  "schemaVersion": 42,
  "tags": [],
  "templating": {
    "list": [
      {
        "allowCustomValue": false,
        "current": {
          "text": "tempo",
          "value": "afad43zq5w5c0e"
        },
        "description": "",
        "label": "tempo_db",
        "name": "tempo_db",
        "options": [],
        "query": "tempo",
        "refresh": 1,
        "regex": "",
        "type": "datasource"
      },
      {
        "current": {
          "text": "63564349b948f4899014c1a21f64bbf8",
          "value": "63564349b948f4899014c1a21f64bbf8"
        },
        "label": "trace_id",
        "name": "trace_id",
        "options": [],
        "query": "",
        "type": "custom"
      },
      {
        "allValue": ".*",
        "allowCustomValue": false,
        "current": {
          "text": "All",
          "value": "$__all"
        },
        "datasource": {
          "type": "prometheus",
          "uid": "prometheus"
        },
        "definition": "label_values(airflow_dagrun_duration_sum,dag_id)",
        "includeAll": true,
        "label": "dag_id",
        "name": "dag_id",
        "options": [],
        "query": {
          "qryType": 1,
          "query": "label_values(airflow_dagrun_duration_sum,dag_id)",
          "refId": "PrometheusVariableQueryEditor-VariableQuery"
        },
        "refresh": 2,
        "regex": "",
        "type": "query"
      }
    ]
  },
  "time": {
    "from": "now-6h",
    "to": "now"
  },
  "timepicker": {},
  "timezone": "browser",
  "title": "Airflow tracing",
  "uid": "90e703ae-c528-46cc-963f-c8d60a139fdb",
  "version": 14
}
