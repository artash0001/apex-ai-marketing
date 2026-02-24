'use strict';

const path = require('path');
const Debug = require('debug');
const fs = require('fs');
const chalk = require('chalk');

function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e["default"] : e; }

const path__default = /*#__PURE__*/_interopDefaultLegacy(path);
const Debug__default = /*#__PURE__*/_interopDefaultLegacy(Debug);
const fs__default = /*#__PURE__*/_interopDefaultLegacy(fs);
const chalk__default = /*#__PURE__*/_interopDefaultLegacy(chalk);

const Prerenderer = require("@prerenderer/prerenderer");
const PuppeteerRenderer = require("@prerenderer/renderer-puppeteer");
const { minify } = require("html-minifier");
const mkdirp = require("mkdirp");
const debug = Debug__default.debug("vite-plugin-prerender");
const compilerFS = fs__default;
function vitePrerender(options) {
  let config;
  const emptyPlugin = {
    name: "vite:prerender"
  };
  debug("plugin options:", options);
  const { _options } = initOptions(options);
  return {
    ...emptyPlugin,
    apply: "build",
    enforce: "post",
    configResolved(resolvedConfig) {
      config = resolvedConfig;
      path__default.isAbsolute(config.build.outDir) ? config.build.outDir : path__default.join(config.root, config.build.outDir);
      debug("resolvedConfig:", resolvedConfig);
    },
    async closeBundle() {
      await emitRendered(_options);
    }
  };
}
const initOptions = (...args) => {
  const rendererOptions = {};
  let _options = {};
  if (args.length === 1) {
    _options = args[0] || {};
  } else {
    console.warn("[vite-plugin-prerender] You appear to be using the v2 argument-based configuration options. It's recommended that you migrate to the clearer object-based configuration system.\nCheck the documentation for more information.");
    let staticDir, routes;
    args.forEach((arg) => {
      if (typeof arg === "string")
        staticDir = arg;
      else if (Array.isArray(arg))
        routes = arg;
      else if (typeof arg === "object")
        _options = arg;
    });
    staticDir ? _options.staticDir = staticDir : null;
    routes ? _options.routes = routes : null;
  }
  if (_options.captureAfterDocumentEvent) {
    console.warn("[vite-plugin-prerender] captureAfterDocumentEvent has been renamed to renderAfterDocumentEvent and should be moved to the renderer options.");
    rendererOptions.renderAfterDocumentEvent = _options.captureAfterDocumentEvent;
  }
  if (_options.captureAfterElementExists) {
    console.warn("[vite-plugin-prerender] captureAfterElementExists has been renamed to renderAfterElementExists and should be moved to the renderer options.");
    rendererOptions.renderAfterElementExists = _options.captureAfterElementExists;
  }
  if (_options.captureAfterTime) {
    console.warn("[vite-plugin-prerender] captureAfterTime has been renamed to renderAfterTime and should be moved to the renderer options.");
    rendererOptions.renderAfterTime = _options.captureAfterTime;
  }
  _options.server = _options.server || {};
  _options.renderer = _options.renderer || new PuppeteerRenderer(Object.assign({}, { headless: true }, rendererOptions));
  if (_options.postProcessHtml) {
    console.warn("[vite-plugin-prerender] postProcessHtml should be migrated to postProcess! Consult the documentation for more information.");
  }
  return { rendererOptions, _options };
};
const emitRendered = (options) => {
  const PrerendererInstance = new Prerenderer(options);
  PrerendererInstance.initialize().then(() => {
    console.log(chalk__default.cyan(`[vite-plugin-prerender] Rendering routes [${chalk__default.green(`${options.routes.join(", ")}`)}] with puppeteer...`));
    return PrerendererInstance.renderRoutes(options.routes || []);
  }).then((renderedRoutes) => {
    console.log(chalk__default.green(`[vite-plugin-prerender] All routes rendered successfully!`));
    if (options.postProcessHtml) {
      console.log(chalk__default.cyan(`[vite-plugin-prerender] Postprocessing rendered html files...`));
      return renderedRoutes.map((renderedRoute) => {
        const processed = options.postProcessHtml(renderedRoute);
        if (typeof processed === "string")
          renderedRoute.html = processed;
        else
          renderedRoute = processed;
        return renderedRoute;
      });
    } else {
      return renderedRoutes;
    }
  }).then((renderedRoutes) => {
    if (options.postProcess) {
      console.log(chalk__default.cyan(`[vite-plugin-prerender] Postprocessing rendered html files...`));
      return Promise.all(renderedRoutes.map((renderedRoute) => options.postProcess(renderedRoute)));
    } else {
      return renderedRoutes;
    }
  }).then((renderedRoutes) => {
    const isValid = renderedRoutes.every((r) => typeof r === "object");
    if (!isValid) {
      throw new Error("[vite-plugin-prerender] Rendered routes are empty, did you forget to return the `context` object in postProcess?");
    }
    return renderedRoutes;
  }).then((renderedRoutes) => {
    if (!options.minify)
      return renderedRoutes;
    console.log(chalk__default.cyan(`[vite-plugin-prerender] minifying rendered html files...`));
    renderedRoutes.forEach((route) => {
      route.html = minify(route.html, options.minify);
    });
    return renderedRoutes;
  }).then((renderedRoutes) => {
    renderedRoutes.forEach((rendered) => {
      if (!rendered.outputPath) {
        rendered.outputPath = path__default.join(options.outputDir || options.staticDir, rendered.route, "index.html");
      }
    });
    return renderedRoutes;
  }).then((processedRoutes) => {
    console.log(chalk__default.cyan(`[vite-plugin-prerender] Generating rendered html files...`));
    const promises = Promise.all(processedRoutes.map((processedRoute) => {
      return mkdirp(path__default.dirname(processedRoute.outputPath)).then(() => {
        return new Promise((resolve, reject) => {
          compilerFS.writeFile(processedRoute.outputPath, processedRoute.html.trim(), (err) => {
            if (err)
              reject(`[vite-plugin-prerender] Unable to write rendered route to file "${processedRoute.outputPath}" 
 ${err}.`);
            else {
              resolve();
            }
          });
        });
      }).catch((err) => {
        if (typeof err === "string") {
          err = `[vite-plugin-prerender] Unable to create directory ${path__default.dirname(processedRoute.outputPath)} for route ${processedRoute.route}. 
 ${err}`;
        }
        throw err;
      });
    }));
    return promises;
  }).then((r) => {
    PrerendererInstance.destroy();
    console.log(chalk__default.green(`[vite-plugin-prerender] All done`));
  }).catch((err) => {
    PrerendererInstance.destroy();
    const msg = "[vite-plugin-prerender] Unable to prerender all routes!";
    console.error(msg);
  });
};
vitePrerender.PuppeteerRenderer = PuppeteerRenderer;

module.exports = vitePrerender;
