define(function(require, exports, module) {
    main.consumes = [
        "c9", "Previewer", "fs", "dialog.error", "commands", "tabManager",
        "layout", "settings", "vfs",
        "menus", "ui"
    ];
    main.provides = ["preview.markdown"];
    return main;

    function main(options, imports, register) {
        var c9 = imports.c9;
        var Previewer = imports.Previewer;
        var fs = imports.fs;
        var showError = imports["dialog.error"].show;
        var commands = imports.commands;
        var tabManager = imports.tabManager;
        var layout = imports.layout;
        var settings = imports.settings;
        var vfs = imports.vfs;
        var menus = imports.menus;
        var ui = imports.ui;

        var highlighter = require("ace/ext/static_highlight");
        var modelist = require("ace/ext/modelist");
        
        /***** Initialization *****/
        
        var plugin = new Previewer("Ajax.org", main.consumes, {
            caption: "Beagle Markdown",
            index: 100,
            selector: function(path) {
                return path && path.match(/(?:\.md|\.markdown)$/i);
            }
        });
        var emit = plugin.getEmitter();
        
        var BGCOLOR = { 
            "flat-light": "rgb(255,255,255)", 
            "flat-dark": "rgba(255, 255, 255, 0.88)",
            "light": "rgba(255, 255, 255, 0.88)", 
            "light-gray": "rgba(255, 255, 255, 0.88)",
            "dark": "rgba(255, 255, 255, 0.88)",
            "dark-gray": "rgba(255, 255, 255, 0.88)" 
        };

        var counter = 0;
        var HTMLURL, previewOrigin;

        /***** Methods *****/
        
        function getPreviewUrl(fn) {
            /*global location*/
            if (options.local && document.baseURI.substr(0, 5) == "file:")
                return setTimeout(getPreviewUrl.bind(null, fn), 100);
            else if (HTMLURL)
                return fn(HTMLURL);
            
            HTMLURL = vfs.serviceUrl
                + "/workspace/.c9/plugins/beagle.bone101/markdown.html"
                + "?host=" + (options.local ? "local" : location.origin);
                
            if (HTMLURL.charAt(0) == "/")
                HTMLURL = location.protocol + "//" + location.host + HTMLURL;
    
            previewOrigin = HTMLURL.match(/^(?:[^\/]|\/\/)*/)[0];
            
            fn(HTMLURL);
        }
        
        function enableScroll(session) {
            if (!session.previewTab || !session.previewTab.loaded)
                return;
            if (session.scrollHook && session.scrollHook == session.previewTab)
                return;
               
            var aceSession = session.previewTab.document.getSession().session;
            if (!aceSession) return;
                
            var listen = function(scrollTopPx) {
                if (!session.source) return; // Renderer is not loaded yet

                var visibleRow = aceSession.c9doc.editor.ace.renderer.getFirstFullyVisibleRow();
                setTimeout(function() {
                    session.source.postMessage({
                        type: "scroll",
                        lineNumber: visibleRow
                    }, "*");
                });
            };
            
            aceSession.on("changeScrollTop", listen);
            session.previewTab.on("unload", function() {
                aceSession.removeListener("changeScrollTop", listen);
            });
            
            session.scrollHook = session.previewTab;
        }

        function bone101(page) {
            switch(page) {
            case "about":
                tabManager.preview({
                    "path": "/About.md",
                    "editorType": "preview",
                    "active": true,
                    "focus": true
                }, function(err, tab) {
                    if (err) return console.error(err);
                });
                break;
            case "intro":
                tabManager.preview({
                    "path": "/Introduction.md",
                    "editorType": "preview",
                    "active": true,
                    "focus": true
                }, function(err, tab) {
                    if (err) return console.error(err);
                });
                break;
            case "examples":
                tabManager.preview({
                    "path": "/README.md",
                    "editorType": "preview",
                    "active": true,
                    "focus": true
                }, function(err, tab) {
                    if (err) return console.error(err);
                });
                break;
            case "node-red":
                tabManager.preview({
                    "path": "/extras/node-red.html",
                    "editorType": "preview",
                    "active": true,
                    "focus": true
                }, function(err, tab) {
                    if (err) return console.error(err);
                });
                break;
            case "mjpg-stream":
                tabManager.preview({
                    "path": "/extras/mjpg-stream.html",
                    "editorType": "preview",
                    "active": true,
                    "focus": true
                }, function(err, tab) {
                    if (err) return console.error(err);
                });
                break;
            default:
            }
        }

        /***** Lifecycle *****/
        
        plugin.on("load", function() {
            console.log("bone101: load");
            commands.addCommand({
                name: "bone101_about",
                isAvailable: function(){ return true; },
                exec: function() {
                    bone101("about");
                }
            }, plugin);
            commands.addCommand({
                name: "bone101_intro",
                isAvailable: function(){ return true; },
                exec: function() {
                    bone101("intro");
                }
            }, plugin);
            commands.addCommand({
                name: "bone101_examples",
                isAvailable: function(){ return true; },
                exec: function() {
                    bone101("examples");
                }
            }, plugin);
            commands.addCommand({
                name: "bone101_node-red",
                isAvailable: function(){ return true; },
                exec: function() {
                    bone101("node-red");
                }
            }, plugin);
            commands.addCommand({
                name: "bone101_mjpg-stream",
                isAvailable: function(){ return true; },
                exec: function() {
                    bone101("mjpg-stream");
                }
            }, plugin);

            menus.addItemByPath("BeagleBone", null, 20, plugin);
            menus.addItemByPath("BeagleBone/About",new ui.item({
                command: "bone101_about"
            }), 22, plugin);
            menus.addItemByPath("BeagleBone/Introduction", new ui.item({
                command: "bone101_intro"
            }), 24, plugin);
            menus.addItemByPath("BeagleBone/Examples", new ui.item({
                command: "bone101_examples"
            }), 26, plugin);
            menus.addItemByPath("BeagleBone/Node-RED", new ui.item({
                command: "bone101_node-red"
            }), 28, plugin);
            menus.addItemByPath("BeagleBone/MJPG-Streamer", new ui.item({
                command: "bone101_mjpg-stream"
            }), 30, plugin);
        });
        plugin.on("sessionStart", function(e) {
            var doc = e.doc;
            var session = e.session;
            var tab = e.tab;
            var editor = e.editor;
            
            if (session.iframe) {
                session.editor = editor;
                editor.container.appendChild(session.iframe);
                return;
            }
            
            var iframe = document.createElement("iframe");
            
            iframe.setAttribute("nwfaketop", true);
            iframe.setAttribute("nwdisable", true);

            iframe.style.width = "100%";
            iframe.style.height = "100%";
            iframe.style.border = 0;
            
            function setTheme(e) {
                iframe.style.backgroundColor = BGCOLOR[e.theme];
            }
            layout.on("themeChange", setTheme, doc);
            setTheme({ theme: settings.get("user/general/@skin") });
            
            if (options.local) {
                iframe.addEventListener("load", function() {
                    // @todo to do this correctly stack needs to allow switching previewer
                    // plugin.activeSession.add(iframe.contentWindow.location.href);
                    
                    iframe.contentWindow.opener = window;
                    if (iframe.contentWindow.start)
                        iframe.contentWindow.start(window);
                });
            }
            
            var onMessage = function(e) {
                if (c9.hosted && e.origin !== previewOrigin)
                    return;
                
                if (e.data.id != session.id)
                    return;
                
                if (e.data.message == "exec") {
                    commands.exec(e.data.command);
                }
                else if (e.data.message == "focus") {
                    tabManager.focusTab(tab);
                }
                else if (e.data.message == "highlight") {
                    var mode = (modelist.modesByName[e.data.lang] 
                        || modelist.getModeForPath("file." + e.data.lang) 
                        || 0).mode || "ace/mode/" + e.data.lang;
                    var theme = "ace/theme/cloud9_day";
                    var value = e.data.content.replace(/[\n\r]*$/, "");
                    
                    highlighter.render(value, mode, theme, 0, true, function (highlighted) {
                        session.source.postMessage({
                            type: "highlight",
                            hid: e.data.hid,
                            html: highlighted.html,
                            css: highlighted.css
                        }, "*");
                    });
                }
                else if (e.data.message == "stream.document") {
                    session.source = e.source;
                    
                    if (session.previewTab) {
                        var doc = session.previewTab.document;
                        
                        if (!doc.hasValue())
                            doc.once("setValue", function() {
                                emit("update", { previewDocument: doc });
                            });
                        else
                            emit("update", { previewDocument: doc });
                    }
                    else {
                        //showError("Testing: " + session.path);
                        fs.stat(session.path, function (err, data) {
                            if (err)
                                return showError(err.message);
                                    
                            if(data.mime == "inode/directory") {
                                fs.readFile(session.path+"/README.md", function(err, data) {
                                    if (err)
                                        return showError(err.message);
                                    
                                    session.source.postMessage({
                                        type: "document",
                                        content: data
                                    }, "*");
                                });
                            } else {
                                fs.readFile(session.path, function(err, data) {
                                    if (err)
                                        return showError(err.message);
                                    
                                    session.source.postMessage({
                                        type: "document",
                                        content: data
                                  }, "*");
                                });
                            }
                        });
                    }
                    
                    session.source.postMessage({
                        type: "keys",
                        keys: commands.getExceptionBindings()
                    }, "*");
                    
                    tab.classList.remove("loading");
                }
            };
            window.addEventListener("message", onMessage, false);
            
            // Set iframe
            session.iframe = iframe;
            session.id = "markdown" + counter++;
            
            session.destroy = function() {
                delete session.editor;
                delete session.iframe;
                
                window.removeEventListener("message", onMessage, false);
            };
            
            // Load the markup renderer
            getPreviewUrl(function(url) { 
                iframe.src = url + "&id=" + session.id; 
            });
            
            session.editor = editor;
            editor.container.appendChild(session.iframe);
        });
        plugin.on("sessionEnd", function(e) {
            var tab = e.tab;
            var session = e.session;
            var iframe = session.iframe;
            
            iframe.parentNode.removeChild(iframe);
            
            tab.classList.remove("loading");
        });
        plugin.on("sessionActivate", function(e) {
            var session = e.session;
            
            session.iframe.style.display = "block";
            session.editor.setLocation(session.path);
            session.editor.setButtonStyle("Markdown", "page_white.png");
        });
        plugin.on("sessionDeactivate", function(e) {
            var session = e.session;
            session.iframe.style.display = "none";
        });
        plugin.on("navigate", function(e) {
            var tab = plugin.activeDocument.tab;
            var iframe = plugin.activeSession.iframe;
            var editor = plugin.activeSession.editor;
            var session = e.session;
            
            tab.classList.add("loading");
            
            tab.title = 
            tab.tooltip = "[M] " + e.url;
            editor.setLocation(e.url);
            
            iframe.src = iframe.src;
            
           enableScroll(session);
        });
        plugin.on("update", function(e) {
            var session = plugin.activeSession;
            if (!session.source) return; // Renderer is not loaded yet
    
            session.source.postMessage({
                type: "document",
                content: e.previewDocument.value,
                fontSize: settings.get("user/ace/fontSize"),
                fontFamily: settings.get("user/ace/fontFamily")
            }, "*");
            
           enableScroll(session);

if(0) { // not working right now, but also don't know that it is needed
            setTimeout(function() {
                if (!session.previewTab || !session.previewTab.loaded) 
                    return;
                
                var doc = session.previewTab.document;
                doc.getSession().session._emit("changeScrollTop");
            }, 100);
}
        });
        plugin.on("reload", function() {
            var iframe = plugin.activeSession.iframe;
            var tab = plugin.activeDocument.tab;
            tab.classList.add("loading");
            iframe.src = iframe.src;
        });
        plugin.on("popout", function() {
            var src = plugin.activeSession.iframe.src;
            window.open(src);
        });
        plugin.on("enable", function() {
            console.log("beagle.bone101: enabled");
        });
        plugin.on("disable", function() {
            console.log("beagle.bone101: disabled")
        });
        plugin.on("unload", function() {
        });
        
        /***** Register and define API *****/
        
        /**
         * Previewer for markdown content.
         **/
        plugin.freezePublicAPI({
        });

        // Cannot quite figure out what event to do this on
        setTimeout(function() {
            bone101("intro");
        }, 500);

        register(null, {
            "preview.markdown": plugin
        });
    }
});
