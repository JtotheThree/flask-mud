module.exports = { contents: "\"use strict\";\nObject.defineProperty(exports, \"__esModule\", { value: true });\nconst jquery = require(\"jquery\");\nrequire(\"../sass/main.scss\");\nconst play_1 = require(\"./play\");\nwindow.$ = jquery;\nwindow.play = new play_1.Play();\nwindow.onload = () => {\n    console.log(\"Window loaded.\");\n};\n",
dependencies: ["jquery","../sass/main.scss","./play"],
sourceMap: {},
headerContent: undefined,
mtime: 1521172393954,
devLibsRequired : undefined,
ac : undefined,
_ : {}
}
