/**
 * Live Python cells inside a pair presentation.html.
 * Standalone: «Ноутбук» toggle (like the journal header). ?notebook=1 opens immediately.
 * Journal iframe uses embed=1: parent FileViewer posts {type:"lh-notebook"} and this file
 * hides the in-page toggle so the button is not duplicated.
 */
(function () {
  "use strict";

  var PYODIDE_INDEX_URL = "https://cdn.jsdelivr.net/pyodide/v0.27.5/full/";
  var RUN_LABEL = "Запуск";
  var UNAVAILABLE =
    "Пакет недоступний у браузерному Python (Pyodide). torch, tensorflow і корпуси nltk тут не запускаються.";
  var INPUT_BLOCKED = "інтерактивне введення в цій версії недоступне";
  var MAX_PAIR_FILE_BYTES = 2 * 1024 * 1024;
  var PAIR_WORK_DIR = "/home/pyodide/work";
  var PYTHON_LANG = /\blanguage-python\b|\blanguage-py\b/;
  var PYTHON_START = /^\s*(import |from |def |class |print\(|np\.|pd\.|plt\.)/m;
  var MOUNT_EXT = {
    ".csv": 1,
    ".txt": 1,
    ".tsv": 1,
    ".json": 1,
    ".py": 1,
    ".png": 1,
    ".jpg": 1,
    ".jpeg": 1,
    ".gif": 1,
    ".webp": 1,
    ".svg": 1,
  };
  var SKIP_NAMES = {
    "presentation.html": 1,
    "teacher.md": 1,
    "plan.json": 1,
    "manifest.json": 1,
    "term-glossary.js": 1,
    "pair-notebook.js": 1,
    "SLOVNYK_TERMINOLOGII.html": 1,
    "SLOVNYK_TERMINOLOGII.md": 1,
  };

  var HELPERS =
    "import ast, base64, io, json, os, sys, traceback\n" +
    "\n" +
    "def _lh_blocked_input(*args, **kwargs):\n" +
    "    raise RuntimeError(" +
    JSON.stringify(INPUT_BLOCKED) +
    ")\n" +
    "\n" +
    "try:\n" +
    "    import builtins as _lh_builtins\n" +
    "except ImportError:\n" +
    "    _lh_builtins = __builtins__\n" +
    "if not isinstance(_lh_builtins, dict):\n" +
    "    _lh_builtins.input = _lh_blocked_input\n" +
    "else:\n" +
    "    _lh_builtins['input'] = _lh_blocked_input\n" +
    "\n" +
    "_LH_KEEP = frozenset(list(globals().keys()) + ['_LH_KEEP', '_lh_run_cell_json', '_lh_reset_user', '_lh_blocked_input'])\n" +
    "\n" +
    "def _lh_run_cell_json(source):\n" +
    "    stdout = io.StringIO()\n" +
    "    stderr = io.StringIO()\n" +
    "    oldout, olderr = sys.stdout, sys.stderr\n" +
    "    sys.stdout, sys.stderr = stdout, stderr\n" +
    "    result_repr = None\n" +
    "    error = None\n" +
    "    try:\n" +
    "        tree = ast.parse(source)\n" +
    "        if tree.body:\n" +
    "            last = tree.body[-1]\n" +
    "            if isinstance(last, ast.Expr):\n" +
    "                body = tree.body[:-1]\n" +
    "                if body:\n" +
    "                    exec(compile(ast.Module(body, type_ignores=[]), '<cell>', 'exec'), globals())\n" +
    "                value = eval(compile(ast.Expression(last.value), '<cell>', 'eval'), globals())\n" +
    "                if value is not None:\n" +
    "                    result_repr = repr(value)\n" +
    "            else:\n" +
    "                exec(compile(tree, '<cell>', 'exec'), globals())\n" +
    "    except Exception:\n" +
    "        error = traceback.format_exc()\n" +
    "    finally:\n" +
    "        sys.stdout, sys.stderr = oldout, olderr\n" +
    "    images = []\n" +
    "    try:\n" +
    "        import matplotlib\n" +
    "        matplotlib.use('Agg')\n" +
    "        import matplotlib.pyplot as plt\n" +
    "        for num in list(plt.get_fignums()):\n" +
    "            fig = plt.figure(num)\n" +
    "            buf = io.BytesIO()\n" +
    "            fig.savefig(buf, format='png', bbox_inches='tight')\n" +
    "            images.append(base64.b64encode(buf.getvalue()).decode('ascii'))\n" +
    "        plt.close('all')\n" +
    "    except Exception:\n" +
    "        pass\n" +
    "    return json.dumps({\n" +
    "        'stdout': stdout.getvalue(),\n" +
    "        'stderr': stderr.getvalue(),\n" +
    "        'result': result_repr,\n" +
    "        'error': error,\n" +
    "        'images': images,\n" +
    "    })\n";

  var CELL_CSS =
    ".lh-nb-cell{margin:.85rem 0;border:1px solid var(--accent,#7dffb3);border-radius:10px;background:var(--panel,#18211c);overflow:hidden;max-width:100%}" +
    ".lh-nb-cell:first-child{margin-top:0}" +
    ".lh-nb-toolbar{display:flex!important;align-items:center;gap:8px;padding:8px 10px;border-bottom:1px solid var(--line,#2f4137);background:#101713}" +
    ".lh-nb-in{font-family:var(--mono,ui-monospace,Menlo,monospace);color:var(--accent,#7dffb3);font-size:.78rem;font-weight:700}" +
    ".lh-nb-run{margin-left:auto;border:0!important;background:#7dffb3!important;color:#062416!important;font:800 .82rem var(--font,inherit)!important;letter-spacing:.04em;text-transform:uppercase;padding:.4rem .9rem!important;min-height:36px;border-radius:8px;cursor:pointer;display:inline-flex!important;align-items:center;visibility:visible!important;opacity:1!important}" +
    ".lh-nb-run:disabled{opacity:.7!important;cursor:wait}" +
    ".lh-nb-source{display:block;width:100%;box-sizing:border-box;border:0;background:#101713;color:var(--ink,#e8f0e7);font-family:var(--mono,ui-monospace,Menlo,monospace);font-size:.82rem;line-height:1.45;padding:10px 12px;resize:vertical;min-height:12rem;flex:1 1 auto;outline:none}" +
    ".lh-nb-output{border-top:1px solid var(--line,#2f4137);padding:8px 12px;font-family:var(--mono,ui-monospace,Menlo,monospace);font-size:.8rem;line-height:1.45;white-space:pre-wrap;overflow:auto;max-height:50%;flex:0 1 auto;color:var(--ink,#e8f0e7)}" +
    ".lh-nb-output[hidden]{display:none!important}" +
    ".lh-nb-output.is-error{color:#ff8fab}" +
    ".lh-nb-output img{display:block;max-width:100%;height:auto;margin-top:.5rem;background:#fff;border-radius:6px}" +
    "article.block>.lh-nb-side,.stage>.block>.lh-nb-side{display:none}" +
    "html.lh-nb-open article.block,html.lh-nb-open .stage>.block{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:stretch}" +
    "html.lh-nb-open article.block[hidden],html.lh-nb-open .stage>.block[hidden]{display:none!important}" +
    "html.lh-nb-open article.block>.lh-nb-main,html.lh-nb-open .stage>.block>.lh-nb-main{min-width:0}" +
    "html.lh-nb-open article.block>.lh-nb-side,html.lh-nb-open .stage>.block>.lh-nb-side{display:flex;flex-direction:column;min-width:0;min-height:100%;padding:.85rem 1rem 1.1rem;border-left:1px solid var(--line,#2f4137);background:#101713}" +
    "html.lh-nb-open .lh-nb-cell{display:flex;flex-direction:column;flex:1 1 auto;min-height:0}" +
    "html.lh-nb-open .lh-nb-main pre[data-lh-nb-cloned='1']{display:none}" +
    "#lh-nb-engine{margin:0 0 .75rem;padding:.55rem .8rem;border:1px solid var(--line,#2f4137);border-radius:10px;background:#101713;color:var(--mute,#9aafa0);font-size:.82rem}" +
    "html.lh-nb-open #lh-nb-engine{display:block}#lh-nb-engine{display:none}" +
    ".lh-nb-toggle{border:1px solid var(--line,#2f4137);background:var(--panel,#18211c);color:var(--ink,#e8f0e7);font:800 .82rem var(--font,inherit);letter-spacing:.04em;padding:.45rem .95rem;min-height:36px;border-radius:10px;cursor:pointer}" +
    ".lh-nb-toggle.is-pressed{background:rgba(125,255,179,.18);color:var(--accent,#7dffb3);border-color:rgba(125,255,179,.55)}" +
    ".rail .lh-nb-toggle{display:inline-flex;align-items:center;justify-content:center;width:100%;margin:0 0 .85rem;box-sizing:border-box}" +
    ".mobile-bar .lh-nb-toggle{flex:0 0 auto;margin-left:auto}" +
    "#lh-nb-toggle-fallback{position:fixed;top:12px;right:12px;z-index:80}" +
    "html.lh-nb-journal-embed .lh-nb-toggle{display:none!important}" +
    "@media (max-width:900px){html.lh-nb-open article.block,html.lh-nb-open .stage>.block{grid-template-columns:minmax(0,1fr)}html.lh-nb-open article.block>.lh-nb-side,html.lh-nb-open .stage>.block>.lh-nb-side{border-left:0;border-top:1px solid var(--line,#2f4137)}}";

  var TOGGLE_LABEL = "Ноутбук";
  var TOGGLE_STORAGE = "lh.nb.open";

  function journalEmbed() {
    try {
      return new URLSearchParams(window.location.search).get("embed") === "1";
    } catch {
      return false;
    }
  }

  function wantOpenInitially() {
    var query = new URLSearchParams(window.location.search);
    if (query.get("notebook") === "1") return true;
    if (query.get("embed") === "1") return false;
    try {
      return window.localStorage.getItem(TOGGLE_STORAGE) === "1";
    } catch {
      return false;
    }
  }

  function persistOpen(open) {
    if (journalEmbed()) return;
    try {
      window.localStorage.setItem(TOGGLE_STORAGE, open ? "1" : "0");
    } catch {
      /* ignore quota / private mode */
    }
  }

  function syncToggleButtons(open) {
    var nodes = document.querySelectorAll(".lh-nb-toggle");
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].setAttribute("aria-pressed", open ? "true" : "false");
      nodes[i].classList.toggle("is-pressed", Boolean(open));
    }
  }

  function bindToggle(setOpen) {
    if (journalEmbed()) {
      document.documentElement.classList.add("lh-nb-journal-embed");
    }
    document.addEventListener("click", function (event) {
      var btn = event.target.closest && event.target.closest(".lh-nb-toggle");
      if (!btn) return;
      event.preventDefault();
      setOpen(!document.documentElement.classList.contains("lh-nb-open"));
    });
    if (journalEmbed() || document.querySelector(".lh-nb-toggle")) return;
    var fallback = document.createElement("button");
    fallback.type = "button";
    fallback.id = "lh-nb-toggle-fallback";
    fallback.className = "lh-nb-toggle";
    fallback.textContent = TOGGLE_LABEL;
    fallback.setAttribute("aria-pressed", "false");
    fallback.title = "Показати код у комірках";
    document.body.appendChild(fallback);
  }

  function sessionId() {
    try {
      var key = "lh.nb.session";
      var existing = window.localStorage.getItem(key);
      if (existing) return existing;
      var id = "s" + Math.random().toString(36).slice(2) + Date.now().toString(36);
      window.localStorage.setItem(key, id);
      return id;
    } catch {
      return "default";
    }
  }

  function journalRunUrl() {
    var parts = window.location.pathname.split("/");
    var i = parts.indexOf("courses");
    if (i < 0 || parts[i + 2] !== "pairs") return "";
    return "/api/courses/" + parts[i + 1] + "/pairs/" + parts[i + 3] + "/notebook/run";
  }

  function projectKernelOrigin() {
    return "http://127.0.0.1:8765";
  }

  function showEngine(label) {
    var el = document.getElementById("lh-nb-engine");
    if (!el) {
      el = document.createElement("div");
      el.id = "lh-nb-engine";
      var stage = document.querySelector("main.stage, .stage");
      if (stage) stage.insertBefore(el, stage.firstChild);
      else document.body.insertBefore(el, document.body.firstChild);
    }
    el.textContent = label;
  }

  async function probeEngine() {
    var runUrl = journalRunUrl();
    if (runUrl) {
      try {
        var res = await fetch("/api/notebook/status", { credentials: "same-origin" });
        if (res.ok) {
          var st = await res.json();
          if (st.enabled && st.ready) {
            return {
              engine: "local-python",
              runUrl: runUrl,
              label: "Ядро: локальний Python журналу. Комірки виконуються на цьому компʼютері.",
            };
          }
        }
      } catch {
        /* fall through */
      }
    }
    try {
      var origin = projectKernelOrigin();
      var res2 = await fetch(origin + "/status", { mode: "cors" });
      if (res2.ok) {
        var st2 = await res2.json();
        if (st2.ok) {
          return {
            engine: "project-venv",
            runUrl: origin + "/run",
            label: "Ядро: Python проєкту (venv). Запуск іде в pair_kernel.py.",
          };
        }
      }
    } catch {
      /* fall through */
    }
    return {
      engine: "pyodide",
      runUrl: "",
      label: "Ядро: браузер (Pyodide). torch, tensorflow і nltk тут не запускаються — відкрийте презентацію з venv або локальний журнал.",
    };
  }

  async function runOnHttpKernel(runUrl, source) {
    var response = await fetch(runUrl, {
      method: "POST",
      credentials: runUrl.indexOf("127.0.0.1") >= 0 ? "omit" : "same-origin",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ source: source, session_id: sessionId() }),
    });
    if (!response.ok) {
      var text = await response.text();
      throw new Error(text || "HTTP " + response.status);
    }
    return response.json();
  }

  function fileBase(name) {
    var normalized = String(name || "").replace(/\\/g, "/");
    var parts = normalized.split("/");
    return parts[parts.length - 1] || "";
  }

  function fileExt(name) {
    var base = fileBase(name);
    var dot = base.lastIndexOf(".");
    return dot >= 0 ? base.slice(dot).toLowerCase() : "";
  }

  function shouldMountPairFile(file) {
    var name = String((file && file.name) || "").replace(/\\/g, "/");
    if (!name || name.indexOf("..") >= 0) return false;
    var base = fileBase(name);
    if (SKIP_NAMES[base] || SKIP_NAMES[name]) return false;
    if (/\.(html|md)$/i.test(base)) return false;
    if (!MOUNT_EXT[fileExt(name)]) return false;
    var size = Number(file && file.size);
    if (isFinite(size) && size > MAX_PAIR_FILE_BYTES) return false;
    return true;
  }

  function workPathFor(name) {
    var normalized = String(name || "")
      .replace(/\\/g, "/")
      .replace(/^\/+/, "");
    return PAIR_WORK_DIR + "/" + normalized;
  }

  function looksLikePython(text) {
    return PYTHON_START.test(String(text || ""));
  }

  function isPythonPre(pre) {
    if (!pre || pre.nodeType !== 1) return false;
    if (typeof pre.closest === "function" && pre.closest(".lh-nb-cell")) return false;
    var code = typeof pre.querySelector === "function" ? pre.querySelector("code") : null;
    var codeClass =
      (code && typeof code.getAttribute === "function" && code.getAttribute("class")) ||
      String((code && code.className) || "");
    if (PYTHON_LANG.test(codeClass)) return true;
    return looksLikePython(pre.textContent || "");
  }

  function injectCss() {
    if (document.getElementById("lh-nb-css")) return;
    var style = document.createElement("style");
    style.id = "lh-nb-css";
    style.textContent = CELL_CSS;
    document.head.appendChild(style);
  }

  function fitTextarea(el) {
    if (!el) return;
    el.style.height = "auto";
    var contentH = el.scrollHeight;
    var article = el.closest("article.block") || el.closest(".stage > .block");
    var side = el.closest(".lh-nb-side");
    var half = 0;
    if (article && side) {
      var cellCount = side.querySelectorAll(".lh-nb-cell").length || 1;
      if (cellCount === 1) {
        half = Math.floor(article.getBoundingClientRect().height * 0.5);
      }
    }
    el.style.height = Math.max(contentH, half, 192) + "px";
  }

  function fitAllTextareas() {
    var nodes = document.querySelectorAll(".lh-nb-source");
    for (var i = 0; i < nodes.length; i += 1) fitTextarea(nodes[i]);
  }

  function cellParts(cell) {
    return {
      cell: cell,
      textarea: cell.querySelector(".lh-nb-source"),
      output: cell.querySelector(".lh-nb-output"),
      inLabel: cell.querySelector(".lh-nb-in"),
      runBtn: cell.querySelector(".lh-nb-run"),
    };
  }

  function makeCell(source) {
    var cell = document.createElement("div");
    cell.className = "lh-nb-cell";
    var toolbar = document.createElement("div");
    toolbar.className = "lh-nb-toolbar";
    var inLabel = document.createElement("span");
    inLabel.className = "lh-nb-in";
    inLabel.textContent = "In [ ]";
    var runBtn = document.createElement("button");
    runBtn.type = "button";
    runBtn.className = "lh-nb-run";
    runBtn.textContent = RUN_LABEL;
    toolbar.appendChild(inLabel);
    toolbar.appendChild(runBtn);
    var textarea = document.createElement("textarea");
    textarea.className = "lh-nb-source";
    textarea.spellcheck = false;
    textarea.value = source;
    var output = document.createElement("div");
    output.className = "lh-nb-output";
    output.hidden = true;
    cell.appendChild(toolbar);
    cell.appendChild(textarea);
    cell.appendChild(output);
    fitTextarea(textarea);
    textarea.addEventListener("input", function () {
      fitTextarea(this);
    });
    return cell;
  }

  function fillSide(article) {
    if (article.hidden || article.hasAttribute("hidden")) return;
    var main = article.querySelector(":scope > .lh-nb-main");
    var side = article.querySelector(":scope > .lh-nb-side");
    if (!main || !side) return;
    var pres = main.querySelectorAll("pre");
    for (var i = 0; i < pres.length; i += 1) {
      var pre = pres[i];
      if (!isPythonPre(pre) || pre.dataset.lhNbCloned === "1") continue;
      pre.dataset.lhNbCloned = "1";
      side.appendChild(makeCell(pre.textContent || ""));
    }
  }

  function prepareSplit() {
    var articles = document.querySelectorAll("article.block, .stage > .block");
    for (var i = 0; i < articles.length; i += 1) {
      var article = articles[i];
      if (article.hidden || article.hasAttribute("hidden")) continue;
      if (article.dataset.lhNbSplit === "1") {
        fillSide(article);
        continue;
      }
      article.dataset.lhNbSplit = "1";
      var main = document.createElement("div");
      main.className = "lh-nb-main";
      var side = document.createElement("div");
      side.className = "lh-nb-side";
      while (article.firstChild) {
        main.appendChild(article.firstChild);
      }
      article.appendChild(main);
      article.appendChild(side);
      fillSide(article);
    }
  }

  function renderOutput(output, result) {
    output.replaceChildren();
    var chunks = [];
    if (result.stdout) chunks.push(String(result.stdout).replace(/\n$/, ""));
    if (result.stderr) chunks.push(String(result.stderr).replace(/\n$/, ""));
    if (result.result) chunks.push(result.result);
    var text = chunks.filter(Boolean).join("\n");
    var hasError = Boolean(result.error);
    if (text) {
      output.appendChild(document.createTextNode(text + (hasError ? "\n" : "")));
    }
    if (hasError) {
      output.appendChild(document.createTextNode(result.error));
    }
    var images = result.images || [];
    for (var i = 0; i < images.length; i += 1) {
      var img = document.createElement("img");
      img.alt = "matplotlib";
      img.src = "data:image/png;base64," + images[i];
      output.appendChild(img);
    }
    output.hidden = !text && !hasError && !images.length;
    output.classList.toggle("is-error", hasError);
  }

  function withTimeout(promise, ms, message) {
    return new Promise(function (resolve, reject) {
      var timer = window.setTimeout(function () {
        reject(new Error(message));
      }, ms);
      promise.then(
        function (value) {
          window.clearTimeout(timer);
          resolve(value);
        },
        function (error) {
          window.clearTimeout(timer);
          reject(error);
        }
      );
    });
  }

  function loadPyodideScript() {
    return new Promise(function (resolve, reject) {
      if (typeof window.loadPyodide === "function") {
        resolve();
        return;
      }
      var existing = document.querySelector('script[data-lh-pyodide="1"]');
      if (existing) {
        existing.addEventListener("load", function () {
          resolve();
        }, { once: true });
        existing.addEventListener(
          "error",
          function () {
            reject(new Error("Не вдалося завантажити pyodide.js"));
          },
          { once: true }
        );
        return;
      }
      var script = document.createElement("script");
      script.src = PYODIDE_INDEX_URL + "pyodide.js";
      script.async = true;
      script.dataset.lhPyodide = "1";
      script.onload = function () {
        resolve();
      };
      script.onerror = function () {
        reject(new Error("Не вдалося завантажити pyodide.js"));
      };
      document.head.appendChild(script);
    });
  }

  function looksUnavailable(code, error) {
    return /\b(torch|tensorflow|nltk)\b/i.test(String(code) + "\n" + (error || ""));
  }

  function siblingUrl(name) {
    return new URL(name, window.location.href).href;
  }

  function collectMountNames() {
    var names = {};
    var links = document.querySelectorAll("a[href]");
    for (var i = 0; i < links.length; i += 1) {
      var href = links[i].getAttribute("href") || "";
      if (!href || href.indexOf("://") >= 0 || href.indexOf("..") >= 0) continue;
      var name = href.split("?")[0].split("#")[0];
      if (shouldMountPairFile({ name: name })) names[name] = true;
    }
    return Object.keys(names);
  }

  async function listManifestFiles() {
    try {
      var response = await fetch(siblingUrl("manifest.json"), { credentials: "same-origin" });
      if (!response.ok) return [];
      var data = await response.json();
      var files = Array.isArray(data.files) ? data.files : [];
      return files
        .map(function (item) {
          return item && item.name;
        })
        .filter(Boolean);
    } catch {
      return [];
    }
  }

  function createSession() {
    var pyodide = null;
    var ready = false;
    var busy = false;
    var executionCount = 0;
    var bootPromise = null;

    async function boot() {
      await withTimeout(loadPyodideScript(), 30000, "Таймаут: не вдалося завантажити pyodide.js");
      if (typeof window.loadPyodide !== "function") {
        throw new Error("loadPyodide не з’явився в вікні");
      }
      var runtime = await withTimeout(
        window.loadPyodide({ indexURL: PYODIDE_INDEX_URL }),
        60000,
        "Таймаут: ядро Python не стартувало"
      );
      await runtime.runPythonAsync(HELPERS);
      pyodide = runtime;
      ready = true;
      runtime.loadPackage(["numpy", "pandas", "matplotlib", "scipy", "scikit-learn"]).catch(function () {});
      return runtime;
    }

    async function ensureReady() {
      if (ready && pyodide) return pyodide;
      if (!bootPromise) {
        bootPromise = boot().catch(function (error) {
          bootPromise = null;
          ready = false;
          throw error;
        });
      }
      return bootPromise;
    }

    async function loadImports(runtime, source) {
      if (looksUnavailable(source, "")) {
        throw new Error(UNAVAILABLE);
      }
      try {
        await runtime.loadPackagesFromImports(source);
      } catch (error) {
        var text = (error && error.message) || String(error);
        if (looksUnavailable(source, text) || /No known package/i.test(text)) {
          throw new Error(UNAVAILABLE);
        }
        throw error;
      }
    }

    async function writeFile(runtime, name) {
      if (!shouldMountPairFile({ name: name })) return;
      try {
        var response = await fetch(siblingUrl(name), { credentials: "same-origin" });
        if (!response.ok) return;
        var buffer = new Uint8Array(await response.arrayBuffer());
        if (buffer.byteLength > MAX_PAIR_FILE_BYTES) return;
        var path = workPathFor(name);
        var dir = path.slice(0, path.lastIndexOf("/"));
        runtime.FS.mkdirTree(dir);
        runtime.FS.writeFile(path, buffer);
      } catch {
        /* file:// or missing sibling */
      }
    }

    return {
      get busy() {
        return busy;
      },
      async start() {
        var runtime = await ensureReady();
        runtime.FS.mkdirTree(PAIR_WORK_DIR);
        var names = collectMountNames();
        var fromManifest = await listManifestFiles();
        for (var i = 0; i < fromManifest.length; i += 1) {
          if (names.indexOf(fromManifest[i]) < 0) names.push(fromManifest[i]);
        }
        for (var j = 0; j < names.length; j += 1) {
          await writeFile(runtime, names[j]);
        }
        runtime.runPython("import os; os.chdir(" + JSON.stringify(PAIR_WORK_DIR) + ")");
      },
      async run(source) {
        if (busy) return { skipped: true };
        busy = true;
        try {
          var runtime = await ensureReady();
          await loadImports(runtime, source);
          var raw = runtime.runPython("_lh_run_cell_json(" + JSON.stringify(source) + ")");
          executionCount += 1;
          var parsed = JSON.parse(raw);
          if (parsed.error && looksUnavailable(source, parsed.error)) {
            parsed.error = UNAVAILABLE;
          }
          parsed.count = executionCount;
          return parsed;
        } catch (error) {
          executionCount += 1;
          return {
            stdout: "",
            stderr: "",
            result: null,
            error: (error && error.message) || String(error),
            images: [],
            count: executionCount,
          };
        } finally {
          busy = false;
        }
      },
    };
  }

  function createHybridSession() {
    var pyodide = createSession();
    var engine = { engine: "pyodide", runUrl: "", label: "" };
    var busy = false;
    var executionCount = 0;
    return {
      get busy() {
        return busy || pyodide.busy;
      },
      async start() {
        engine = await probeEngine();
        showEngine(engine.label);
        if (engine.engine === "pyodide") {
          await pyodide.start();
        }
      },
      async run(source) {
        if (engine.engine === "pyodide") {
          return pyodide.run(source);
        }
        if (busy) return { skipped: true };
        busy = true;
        try {
          var parsed = await runOnHttpKernel(engine.runUrl, source);
          executionCount += 1;
          parsed.count = executionCount;
          return parsed;
        } catch (error) {
          executionCount += 1;
          return {
            stdout: "",
            stderr: "",
            result: null,
            error: (error && error.message) || String(error),
            images: [],
            count: executionCount,
          };
        } finally {
          busy = false;
        }
      },
    };
  }

  function bindEvents(session) {
    if (document.documentElement.dataset.lhNbEvents === "1") return;
    document.documentElement.dataset.lhNbEvents = "1";

    async function runFromCell(cell) {
      if (!cell) return;
      var entry = cellParts(cell);
      if (!entry.textarea || session.busy) return;
      if (entry.runBtn) {
        entry.runBtn.disabled = true;
        entry.runBtn.textContent = "…";
      }
      try {
        var result = await session.run(entry.textarea.value);
        if (result.skipped) return;
        if (entry.inLabel) entry.inLabel.textContent = "In [" + result.count + "]";
        renderOutput(entry.output, result);
      } finally {
        if (entry.runBtn) {
          entry.runBtn.disabled = false;
          entry.runBtn.textContent = RUN_LABEL;
        }
      }
    }

    document.addEventListener("click", function (event) {
      var btn = event.target.closest && event.target.closest(".lh-nb-run");
      if (!btn) return;
      runFromCell(btn.closest(".lh-nb-cell"));
    });
    document.addEventListener("keydown", function (event) {
      if (event.key !== "Enter" || !event.shiftKey) return;
      if (!event.target.classList || !event.target.classList.contains("lh-nb-source")) return;
      event.preventDefault();
      runFromCell(event.target.closest(".lh-nb-cell"));
    });
  }

  function boot() {
    injectCss();
    prepareSplit();
    var session = createHybridSession();
    var started = false;
    bindEvents(session);

    function setNotebookOpen(open) {
      document.documentElement.classList.toggle("lh-nb-open", Boolean(open));
      document.body.classList.toggle("lh-nb-open", Boolean(open));
      syncToggleButtons(open);
      persistOpen(open);
      if (open && !started) {
        started = true;
        session.start().catch(function () {});
      }
      if (open) {
        window.requestAnimationFrame(function () {
          fitAllTextareas();
          window.setTimeout(fitAllTextareas, 60);
        });
      }
    }

    bindToggle(setNotebookOpen);
    window.addEventListener("resize", fitAllTextareas);

    window.__lhNotebookSetOpen = setNotebookOpen;
    window.addEventListener("message", function (event) {
      if (event.source !== window.parent) return;
      var data = event.data || {};
      if (data.type !== "lh-notebook") return;
      setNotebookOpen(Boolean(data.open));
    });

    setNotebookOpen(wantOpenInitially());
    window.setTimeout(function () {
      prepareSplit();
      fitAllTextareas();
    }, 50);
    window.setTimeout(function () {
      prepareSplit();
      fitAllTextareas();
    }, 400);
    try {
      var observer = new MutationObserver(prepareSplit);
      observer.observe(document.body, { childList: true, subtree: true });
    } catch {
      /* ignore */
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", boot);
  } else {
    boot();
  }
})();
