var root_url = "http://localhost:5000/";
var selection = "";
var parentDiv;

function contextly(info) {
    chrome.storage.sync.get(["nat_lang"], function(result) {
        var word = info.selectionText;
        chrome.tabs.create({
            url: root_url + word + "?nat_lang=" + result.nat_lang
        });
    });
}

var rule = {
    conditions: [
        new chrome.declarativeContent.PageStateMatcher({
            css: ["body"]
        })
    ],
    actions: [new chrome.declarativeContent.ShowPageAction()]
};

chrome.runtime.onInstalled.addListener(function() {
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
        chrome.declarativeContent.onPageChanged.addRules([rule]);
    });
    chrome.storage.sync.set({ nat_lang: "ko" }, function(result) {
        console.log("nat_lang: " + "ko");
    });
    chrome.contextMenus.create({
        title: "Contextly",
        id: "main",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener(function(info) {
    chrome.tabs.executeScript(
        {
            code: "window.getSelection();"
        },
        function(selection) {
            console.log(selection);
            console.log(selection.toString()[0]);
            var parentDiv = selection.getRangeAt(0).startContainer.parentNode;
            console.log(selection.toString()[0]);
            contextly(info);
        }
    );
});
