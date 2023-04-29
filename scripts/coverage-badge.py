#!/usr/bin/env python3

import json
import sys

TEMPLATE = """
  <svg xmlns="http://www.w3.org/2000/svg" width="105" height="20">
    <title>Coverage - %(percent)s%%</title>
    <defs>
      <linearGradient id="workflow-fill" x1="50%%" y1="0%%" x2="50%%" y2="100%%">
        <stop stop-color="#444D56" offset="0%%"></stop>
        <stop stop-color="#24292E" offset="100%%"></stop>
      </linearGradient>
      <linearGradient id="state-fill" x1="50%%" y1="0%%" x2="50%%" y2="100%%">
        <stop stop-color="#34D058" offset="0%%"></stop>
        <stop stop-color="#28A745" offset="100%%"></stop>
      </linearGradient>
    </defs>
    <g fill="none" fill-rule="evenodd">
      <g font-family="&#39;DejaVu Sans&#39;,Verdana,Geneva,sans-serif" font-size="11">
        <path id="workflow-bg" d="M0,3 C0,1.3431 1.3552,0 3.02702703,0 L65,0 L65,20 L3.02702703,20 C1.3552,20 0,18.6569 0,17 L0,3 Z" fill="url(#workflow-fill)" fill-rule="nonzero"></path>
        <text fill="#010101" fill-opacity=".3">
          <tspan x="6" y="15" aria-hidden="true">Coverage</tspan>
        </text>
        <text fill="#FFFFFF">
          <tspan x="6" y="14">Coverage</tspan>
        </text>
      </g>
      <g transform="translate(65)" font-family="&#39;DejaVu Sans&#39;,Verdana,Geneva,sans-serif" font-size="11">
        <path d="M0 0h46.939C48.629 0 40 1.343 40 3v14c0 1.657-1.37 3-3.061 3H0V0z" id="state-bg" fill="url(#state-fill)" fill-rule="nonzero"></path>
        <text fill="#010101" fill-opacity=".3" aria-hidden="true">
          <tspan x="7" y="15">%(percent_rounded)s%%</tspan>
        </text>
        <text fill="#FFFFFF">
          <tspan x="7" y="14">%(percent_rounded)s%%</tspan>
        </text>
      </g>
    </g>
  </svg>
  """

with open(sys.argv[1], "r", encoding = "utf-8") as f:
  coverage = json.loads(f.read())

with open(sys.argv[2], "w", encoding = "utf-8") as f:
  f.write(
    TEMPLATE % {
      "percent": coverage["totals"]["percent_covered"],
      "percent_rounded": coverage["totals"]["percent_covered_display"]
    }
  )
