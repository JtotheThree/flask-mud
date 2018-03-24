const { FuseBox, CSSPlugin, SassPlugin } = require("fuse-box");
const fuse = FuseBox.init({
    homeDir : "flask_mud/static",
    target: 'browser@es6',
    output: "flask_mud/static/assets/$name.js",
    plugins: [
        [SassPlugin({
            importer: true, 
            macros: {"@daemonite": "node_modules/daemonite-material/assets/scss/"}}), 
        CSSPlugin()],
        CSSPlugin()]
})
fuse.dev({
    port:8080,
    httpServer: false,
});
fuse.bundle("app").instructions(" > /ts/main.ts").hmr().watch()
fuse.run();