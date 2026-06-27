window.momentumOption = {
  "backgroundColor": "transparent",
  "tooltip": {
    "trigger": "axis",
    "backgroundColor": "rgba(5, 11, 24, 0.94)",
    "borderColor": "rgba(132, 234, 255, 0.45)",
    "textStyle": {
      "color": "#eef8ff"
    }
  },
  "grid": {
    "left": 54,
    "right": 28,
    "top": 36,
    "bottom": 72
  },
  "xAxis": {
    "type": "category",
    "data": [
      "Jun 20",
      "Jun 21",
      "Jun 21",
      "Jun 23",
      "Jun 23",
      "Jun 23",
      "Jun 24",
      "Jun 24"
    ],
    "axisLabel": {
      "color": "#9dc4e9",
      "fontSize": 12,
      "interval": 0
    },
    "axisLine": {
      "lineStyle": {
        "color": "rgba(132, 234, 255, 0.35)"
      }
    },
    "axisTick": {
      "show": false
    }
  },
  "yAxis": {
    "type": "value",
    "min": 40,
    "max": 100,
    "name": "stack signal",
    "nameTextStyle": {
      "color": "#9dc4e9"
    },
    "axisLabel": {
      "color": "#9dc4e9"
    },
    "splitLine": {
      "lineStyle": {
        "color": "rgba(132, 234, 255, 0.11)"
      }
    }
  },
  "series": [
    {
      "name": "Milestone",
      "type": "line",
      "smooth": true,
      "symbol": "diamond",
      "symbolSize": 14,
      "lineStyle": {
        "width": 4,
        "color": "#18c8ff"
      },
      "areaStyle": {
        "color": {
          "type": "linear",
          "x": 0,
          "y": 0,
          "x2": 0,
          "y2": 1,
          "colorStops": [
            {
              "offset": 0,
              "color": "rgba(24, 200, 255, 0.32)"
            },
            {
              "offset": 1,
              "color": "rgba(10, 109, 255, 0.02)"
            }
          ]
        }
      },
      "itemStyle": {
        "color": "#18c8ff",
        "borderColor": "#eef8ff",
        "borderWidth": 1
      },
      "label": {
        "show": true,
        "position": "top",
        "color": "#eef8ff",
        "fontSize": 10
      },
      "labelLayout": {
        "hideOverlap": true
      },
      "data": [
        [
          "Jun 20",
          58,
          "Imatrix scale search",
          "864f263",
          "Quant",
          "#84eaff"
        ],
        [
          "Jun 21",
          70,
          "Request-level MTP controls",
          "c226d1f",
          "Serve",
          "#18c8ff"
        ],
        [
          "Jun 21",
          82,
          "Dynamic Drafting",
          "7be6304 / ac7e259",
          "Serve",
          "#18c8ff"
        ],
        [
          "Jun 23",
          84,
          "Decode hot paths",
          "547321d / c3342ee",
          "Kernel",
          "#0a6dff"
        ],
        [
          "Jun 23",
          78,
          "Speculative state safety",
          "c823b4c / 7a4f009",
          "Safety",
          "#7bb7ff"
        ],
        [
          "Jun 23",
          88,
          "Step MTP3 heads",
          "11d76c2",
          "Models",
          "#4fd8ff"
        ],
        [
          "Jun 24",
          92,
          "MTP profiles and preflight",
          "db24788",
          "Proof",
          "#ffffff"
        ],
        [
          "Jun 24",
          86,
          "Benchmark tables",
          "9157acd",
          "Proof",
          "#ffffff"
        ]
      ]
    }
  ]
};

window.momentumOption.tooltip.formatter = function(params) {
  var p = params[0];
  var d = p.data;
  return "<b>" + d[2] + "</b><br/>" + d[0] + " · " + d[4] + "<br/>commit " + d[3] + "<br/>stack signal " + d[1];
};
window.momentumOption.series[0].label.formatter = function(params) {
  return params.data[4];
};
window.momentumOption.series[0].itemStyle.color = function(params) {
  return params.data[5];
};
