define(function(require, exports, module) {
    main.consumes = [
        "Plugin", "ui", "commands", "menus", "tabManager",
        "Previewer", "Editor", "editors", "layout", "settings"
    ];
    main.provides = ["beagle.bone101"];
    return main;

    function main(options, imports, register) {
        var Plugin = imports.Plugin;
        var ui = imports.ui;
        var commands = imports.commands;
        var menus = imports.menus;
        var tabManager = imports.tabManager;
        var Previewer = imports.Previewer;
        var Editor = imports.Editor;
        var editors = imports.editors;
        var layout = imports.layout;
        var settings = imports.settings;
        var path = require("path");

        var basename = path.basename;
        var extensions = ["bone101"];
        var handle = editors.register("bone101", "Bone101", Bone101Editor, extensions);
        console.log("editors: " + JSON.stringify(editors));
        var BGCOLOR = {
            "flat-light": "#F1F1F1",
            "light": "#D3D3D3",
            "light-gray": "#D3D3D3",
            "dark": "#3D3D3D",
            "dark-gray": "#3D3D3D"
        };

        function Bone101Editor(){
            console.log("bone101: build editor");
            var plugin = new Editor("BeagleBoard.org", main.consumes, extensions);

            var container, contents;
            var currentSession, currentDocument;

            plugin.on("draw", function(e) {
                console.log("bone101: draw");
                container = e.htmlNode;
                var tab = e.tab;
                tab.title = "bone101";
                tab.tooltip = "bone101";

                var iframe = document.createElement("iframe");
                iframe.style.width = "100%";
                iframe.style.height = "100%";
                iframe.style.border = 0;
                iframe.src = "http://192.168.6.2";
                container.appendChild(iframe);
            });
            plugin.on("documentLoad", function(e){
                console.log("bone101: documentLoad");
                currentDocument = e.doc;
                currentSession = currentDocument.getSession();
                currentDocument.tab.on("setPath", setTitle, currentSession);
                function setTitle(e) {
                    currentDocument.title = "bone101";
                    currentDocument.tooltip = "bone101";
                }
                setTitle();
            });
            plugin.on("documentActivate", function(e){
                console.log("bone101: documentActivate");
            });
            plugin.on("documentUnload", function(e){
                console.log("bone101: documentUnload");
            });
            plugin.freezePublicAPI({

            });
            plugin.load(null, "beagle.bone101");
            return plugin;
        }

        handle.on("load", function(){
            console.log("bone101: load");
            commands.addCommand({
                name: "bone101_about",
                isAvailable: function(){ return true; },
                exec: function() {
                    bone101("about");
                }
            }, handle);
            commands.addCommand({
                name: "bone101_intro",
                isAvailable: function(){ return true; },
                exec: function() {
                    bone101("intro");
                }
            }, handle);
            bone101("intro");

            menus.addItemByPath("BeagleBone", null, 20, handle);
            menus.addItemByPath("BeagleBone/About",new ui.item({
                command: "bone101_about"
            }), 22, handle);
            menus.addItemByPath("BeagleBone/Introduction", new ui.item({
                command: "bone101_intro"
            }), 24, handle);
        });

        function bone101(page) {
            var filename = options.packagePath + ".bone101";
            console.log("opening " + filename);
            var tab = tabManager.open({
                "path": filename,
                "editorType": "bone101",
                "title": "bone101",
                "tooltip": "bone101",
                "focus": true
            }, function(err, tab){
                if (err) return console.error(err);
            });
        }

        register(null, {
            "beagle.bone101": handle
        });
    }
});