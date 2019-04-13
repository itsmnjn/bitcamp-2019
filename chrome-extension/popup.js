chrome.storage.sync.get(["nat_lang"], function(result) {
    console.log("Value currently is " + result.key);
});
