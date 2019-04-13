var root_url = "http://localhost:5000/";
var selection = "";

function contextly(info) {
    chrome.storage.sync.get(["nat_lang"], function(result) {
        var word = info.selectionText;
        chrome.tabs.create({
            url: root_url + word + "?nat_lang=" + result.nat_lang
        });
    });
}

function getSelected() {
    var userSelection;
    if (window.getSelection) {
        userSelection = window.getSelection();
    } else if (document.selection) {
        userSelection = document.selection.createRange();
    }
    return userSelection;
}

function getSelectedNode() {
    if (document.selection)
        return document.selection.createRange().parentElement();
    else {
        var selection = window.getSelection();
        if (selection.rangeCount > 0)
            return selection.getRangeAt(0).startContainer.parentNode;
    }
}

function storeSelection() {
    return [window.getSelection()];
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

document.addEventListener("mouseup", storeSelection, false);

chrome.contextMenus.onClicked.addListener(function(info) {
    var selection = getSelected() + "";
    var parentDiv = getSelectedNode();
    console.log(document);
    var index = parentDiv.indexOf(selection);
    console.log(parentDiv.substr(0, index));
    contextly(info);
});
