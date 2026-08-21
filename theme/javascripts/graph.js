/* Concept graph explorer.
 *
 * Deliberately dependency-free: a small velocity-Verlet force layout in plain
 * SVG. The graph is a few hundred nodes, which does not justify shipping a
 * charting library, and a self-contained implementation keeps the published
 * site working offline and without a CDN.
 *
 * Node colour encodes `status` (how settled a term is), radius encodes degree.
 */
(function () {
  "use strict";

  var STATUS_ORDER = [
    "foundational", "established", "modern", "emerging", "experimental",
    "informal", "slang", "marketing", "contested", "historical", "deprecated"
  ];

  var LEGEND = [
    ["foundational", "Foundational"],
    ["established", "Established"],
    ["modern", "Modern"],
    ["emerging", "Emerging"],
    ["contested", "Contested"],
    ["slang", "Slang / informal"],
    ["historical", "Historical"]
  ];

  function el(tag, attrs, parent) {
    var node = document.createElementNS("http://www.w3.org/2000/svg", tag);
    for (var key in attrs) node.setAttribute(key, attrs[key]);
    if (parent) parent.appendChild(node);
    return node;
  }

  function statusColour(root, status) {
    var value = getComputedStyle(root).getPropertyValue("--node-" + status);
    return value.trim() || "#888";
  }

  function build(root, data) {
    var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var nodes = data.nodes.map(function (n) { return Object.assign({}, n); });
    var index = {};
    nodes.forEach(function (n, i) { index[n.id] = i; });

    var links = data.links
      .filter(function (l) { return l.source in index && l.target in index; })
      .map(function (l) {
        return { source: index[l.source], target: index[l.target], type: l.type };
      });

    var adjacency = nodes.map(function () { return []; });
    links.forEach(function (l, i) {
      adjacency[l.source].push(i);
      adjacency[l.target].push(i);
    });

    // -- chrome -----------------------------------------------------------
    var controls = document.createElement("div");
    controls.className = "graph-controls";
    controls.innerHTML =
      '<label>Domain <select data-role="category"></select></label>' +
      '<label>Find <input type="search" data-role="search" placeholder="e.g. kv cache" list="graph-terms"></label>' +
      '<datalist id="graph-terms"></datalist>' +
      '<button type="button" data-role="reset">Reset</button>' +
      '<span class="graph-status" data-role="status"></span>';
    root.appendChild(controls);

    var categorySelect = controls.querySelector('[data-role="category"]');
    categorySelect.innerHTML = '<option value="">All domains</option>' +
      data.categories.map(function (c) {
        return '<option value="' + c.id + '">' + c.number + ". " + c.name + "</option>";
      }).join("");

    controls.querySelector("datalist").innerHTML = nodes.map(function (n) {
      return '<option value="' + n.term.replace(/"/g, "&quot;") + '">';
    }).join("");

    var svg = el("svg", { viewBox: "0 0 1000 560", preserveAspectRatio: "xMidYMid meet" });
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", "Concept graph. Use the search field to locate a concept.");
    root.appendChild(svg);

    var legend = document.createElement("div");
    legend.className = "graph-legend";
    legend.innerHTML = LEGEND.map(function (pair) {
      return '<span style="color:' + statusColour(root, pair[0]) + '">' + pair[1] + "</span>";
    }).join("");
    root.appendChild(legend);

    var tooltip = document.createElement("div");
    tooltip.className = "graph-tooltip";
    root.appendChild(tooltip);

    var status = controls.querySelector('[data-role="status"]');

    // -- initial placement: seeded ring per category, so the first frame is
    //    already legible rather than a random explosion --------------------
    var W = 1000, H = 560;
    var catIndex = {};
    data.categories.forEach(function (c, i) { catIndex[c.id] = i; });
    var catCount = Math.max(data.categories.length, 1);

    nodes.forEach(function (n, i) {
      var band = (catIndex[n.category] || 0) / catCount * Math.PI * 2;
      var jitter = (i % 17) / 17;
      var radius = 90 + jitter * 190;
      n.x = W / 2 + Math.cos(band + jitter * 0.9) * radius;
      n.y = H / 2 + Math.sin(band + jitter * 0.9) * radius;
      n.vx = 0;
      n.vy = 0;
      n.r = Math.min(4 + Math.sqrt(n.degree || 1) * 1.9, 15);
    });

    var linkLayer = el("g", { class: "links" }, svg);
    var nodeLayer = el("g", { class: "nodes" }, svg);

    var linkEls = links.map(function () {
      return el("line", { class: "link", "stroke-width": 1 }, linkLayer);
    });

    var nodeEls = nodes.map(function (n) {
      var g = el("g", { class: "node" }, nodeLayer);
      el("circle", { r: n.r, fill: statusColour(root, n.status) }, g);
      var label = el("text", { class: "node-label", dy: -n.r - 4, "text-anchor": "middle" }, g);
      label.textContent = n.term;
      label.style.display = n.degree >= 6 ? "" : "none";
      g.addEventListener("pointerenter", function (event) { showTip(n, event); });
      g.addEventListener("pointerleave", hideTip);
      g.addEventListener("click", function () { window.location.href = n.url; });
      return g;
    });

    function showTip(node, event) {
      tooltip.innerHTML =
        "<strong>" + node.term + "</strong>" +
        '<span class="meta">' + node.status + " · " + node.difficulty + "</span>" +
        "<p>" + node.one_liner + "</p>";
      var box = root.getBoundingClientRect();
      tooltip.style.left = Math.min(event.clientX - box.left + 14, box.width - 340) + "px";
      tooltip.style.top = (event.clientY - box.top + 14) + "px";
      tooltip.style.opacity = "1";
      focus(node.id);
    }

    function hideTip() {
      tooltip.style.opacity = "0";
      if (!pinned) focus(null);
    }

    var pinned = null;

    function focus(id) {
      if (id === null) {
        nodeEls.forEach(function (g) { g.classList.remove("is-dimmed", "is-focused"); });
        linkEls.forEach(function (l) { l.classList.remove("is-highlighted"); });
        return;
      }
      var i = index[id];
      var near = {};
      near[i] = true;
      adjacency[i].forEach(function (li) {
        near[links[li].source] = true;
        near[links[li].target] = true;
      });
      nodeEls.forEach(function (g, j) {
        g.classList.toggle("is-dimmed", !near[j]);
        g.classList.toggle("is-focused", j === i);
      });
      linkEls.forEach(function (l, li) {
        l.classList.toggle("is-highlighted", links[li].source === i || links[li].target === i);
      });
    }

    // -- forces -----------------------------------------------------------
    var alpha = 1;

    function step() {
      var i, j, n, m, dx, dy, dist, force;

      // repulsion, O(n^2) but n is small enough that it stays smooth
      for (i = 0; i < nodes.length; i++) {
        n = nodes[i];
        for (j = i + 1; j < nodes.length; j++) {
          m = nodes[j];
          dx = m.x - n.x;
          dy = m.y - n.y;
          dist = Math.sqrt(dx * dx + dy * dy) || 0.01;
          if (dist > 260) continue;
          force = (900 / (dist * dist)) * alpha;
          dx = (dx / dist) * force;
          dy = (dy / dist) * force;
          n.vx -= dx; n.vy -= dy;
          m.vx += dx; m.vy += dy;
        }
      }

      // springs
      links.forEach(function (l) {
        var a = nodes[l.source], b = nodes[l.target];
        var ddx = b.x - a.x, ddy = b.y - a.y;
        var d = Math.sqrt(ddx * ddx + ddy * ddy) || 0.01;
        var k = ((d - 76) * 0.012) * alpha;
        ddx = (ddx / d) * k;
        ddy = (ddy / d) * k;
        a.vx += ddx; a.vy += ddy;
        b.vx -= ddx; b.vy -= ddy;
      });

      // centring and integration
      nodes.forEach(function (node) {
        node.vx += (W / 2 - node.x) * 0.0016 * alpha;
        node.vy += (H / 2 - node.y) * 0.0016 * alpha;
        node.vx *= 0.86;
        node.vy *= 0.86;
        node.x = Math.max(node.r + 2, Math.min(W - node.r - 2, node.x + node.vx));
        node.y = Math.max(node.r + 12, Math.min(H - node.r - 2, node.y + node.vy));
      });

      alpha *= 0.994;
    }

    function render() {
      nodeEls.forEach(function (g, i) {
        g.setAttribute("transform", "translate(" + nodes[i].x.toFixed(1) + "," + nodes[i].y.toFixed(1) + ")");
      });
      linkEls.forEach(function (line, i) {
        var a = nodes[links[i].source], b = nodes[links[i].target];
        line.setAttribute("x1", a.x.toFixed(1));
        line.setAttribute("y1", a.y.toFixed(1));
        line.setAttribute("x2", b.x.toFixed(1));
        line.setAttribute("y2", b.y.toFixed(1));
      });
    }

    var settleFrames = reduceMotion ? 260 : 0;
    for (var s = 0; s < settleFrames; s++) step();
    render();

    if (!reduceMotion) {
      (function tick() {
        if (alpha > 0.02) {
          step();
          render();
          requestAnimationFrame(tick);
        }
      })();
    }

    // -- interaction ------------------------------------------------------
    function applyFilter(category) {
      var shown = 0;
      nodeEls.forEach(function (g, i) {
        var visible = !category || nodes[i].category === category;
        g.style.display = visible ? "" : "none";
        if (visible) shown++;
      });
      linkEls.forEach(function (line, i) {
        var visible = !category ||
          (nodes[links[i].source].category === category && nodes[links[i].target].category === category);
        line.style.display = visible ? "" : "none";
      });
      status.textContent = shown + " of " + nodes.length + " concepts";
      alpha = Math.max(alpha, 0.5);
      if (reduceMotion) { for (var k = 0; k < 120; k++) step(); render(); }
      else (function tick() {
        if (alpha > 0.02) { step(); render(); requestAnimationFrame(tick); }
      })();
    }

    categorySelect.addEventListener("change", function () {
      applyFilter(this.value);
    });

    controls.querySelector('[data-role="search"]').addEventListener("input", function () {
      var query = this.value.trim().toLowerCase();
      if (!query) { pinned = null; focus(null); return; }
      var hit = nodes.find(function (n) {
        return n.term.toLowerCase() === query || n.id === query.replace(/\s+/g, "-");
      }) || nodes.find(function (n) { return n.term.toLowerCase().indexOf(query) === 0; });
      if (hit) { pinned = hit.id; focus(hit.id); }
    });

    controls.querySelector('[data-role="reset"]').addEventListener("click", function () {
      categorySelect.value = "";
      controls.querySelector('[data-role="search"]').value = "";
      pinned = null;
      focus(null);
      applyFilter("");
    });

    status.textContent = nodes.length + " concepts · " + links.length + " relationships";

    // deep link: graph/?focus=kv-cache
    var wanted = new URLSearchParams(window.location.search).get("focus");
    if (wanted && wanted in index) { pinned = wanted; focus(wanted); }
  }

  function init() {
    var root = document.getElementById("graph-app");
    if (!root || root.dataset.ready) return;
    root.dataset.ready = "1";

    fetch(root.dataset.src)
      .then(function (r) { return r.json(); })
      .then(function (data) { build(root, data); })
      .catch(function () {
        root.innerHTML =
          '<div class="graph-fallback">The graph could not be loaded. ' +
          'The same data is available as JSON at <code>api/graph.json</code>, ' +
          "and every entry lists its relationships directly.</div>";
      });
  }

  document.addEventListener("DOMContentLoaded", init);
  if (window.document$) window.document$.subscribe(init); // Material instant navigation
})();
