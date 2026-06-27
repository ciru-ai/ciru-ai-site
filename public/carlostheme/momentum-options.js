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
      "Jun 5",
      "Jun 10",
      "Jun 11",
      "Jun 13",
      "Jun 13",
      "Jun 20",
      "Jun 23",
      "Jun 23",
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
    "name": "repo signal",
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
          "Jun 5",
          56,
          "Prune ROCmFP4 scale search",
          "27b4801",
          "Backend",
          "#0a6dff"
        ],
        [
          "Jun 10",
          66,
          "Port Qwen/Gemma/Step MTP",
          "e766769",
          "Models",
          "#4fd8ff"
        ],
        [
          "Jun 11",
          70,
          "Add Diffusion Gemma path",
          "2fc27de / 2cc69b7",
          "Models",
          "#4fd8ff"
        ],
        [
          "Jun 13",
          74,
          "Clarify AMD build support",
          "1c566e9",
          "Docs",
          "#ffffff"
        ],
        [
          "Jun 13",
          78,
          "Add CM2 vector decode",
          "1c1d4f5 / 4860505 / 4795079",
          "Backend",
          "#0a6dff"
        ],
        [
          "Jun 20",
          80,
          "Use imatrix scale search",
          "864f263",
          "Format",
          "#84eaff"
        ],
        [
          "Jun 23",
          84,
          "Support EAGLE3 state",
          "7a4f009",
          "Speculative",
          "#7bb7ff"
        ],
        [
          "Jun 23",
          88,
          "Support Step MTP3 heads",
          "11d76c2",
          "Speculative",
          "#7bb7ff"
        ],
        [
          "Jun 24",
          90,
          "Add safety/profile docs",
          "db24788 / 9157acd / e22278e",
          "Docs",
          "#ffffff"
        ]
      ]
    }
  ]
};

window.momentumOption.tooltip.formatter = function(params) {
  var p = params[0];
  var d = p.data;
  return "<b>" + d[2] + "</b><br/>" + d[0] + " · " + d[4] + "<br/>commit " + d[3] + "<br/>repo signal " + d[1];
};
window.momentumOption.series[0].label.formatter = function(params) {
  return params.data[4];
};
window.momentumOption.series[0].itemStyle.color = function(params) {
  return params.data[5];
};
