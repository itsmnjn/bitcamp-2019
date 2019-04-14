var root_url = "http://localhost:5000/";
var sentence = "";

function contextly(info, sentence) {
    chrome.storage.sync.get(["nat_lang"], function(result) {
        var word = info.selectionText;
        chrome.tabs.create({
            url:
                root_url +
                word +
                "?nat_lang=" +
                result.nat_lang +
                "&sentence=" +
                sentence
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

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    console.log(
        sender.tab
            ? "from a content script:" + sender.tab.url
            : "from the extension"
    );
    if (request.sentence) sendResponse({ farewell: "thanks" });
    sentence = request.sentence;
});

chrome.contextMenus.onClicked.addListener(function(info) {
    chrome.tabs.executeScript(
        {
            code: "sendSentence();"
        },
        function() {
            contextly(info, sentence);
        }
    );
});
