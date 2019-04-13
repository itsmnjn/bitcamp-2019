function contextly(info) {
    var word = info.selectionText;
    chrome.tabs.create({ url: "https://google.com/search?q=" + word });
}

var rule = {
    conditions: [
        new chrome.declarativeContent.PageStateMatcher({
            css: ["p"]
        })
    ],
    actions: [new chrome.declarativeContent.ShowPageAction()]
};

chrome.runtime.onInstalled.addListener(function() {
    chrome.storage.sync.set({ nat_lang: "kor" }, function() {
        console.log("Native language: kor");
    });
    chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
        chrome.declarativeContent.onPageChanged.addRules([rule]);
    });
    chrome.contextMenus.create({
        title: "Contextly",
        id: "main",
        contexts: ["selection"]
    });
});

chrome.contextMenus.onClicked.addListener(contextly);
