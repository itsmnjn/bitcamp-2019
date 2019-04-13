function set_lang(lang, list) {
    chrome.storage.sync.set({ nat_lang: lang }, function(result) {
        list.value = lang;
    });
}

var nat_lang_list = document.getElementById("nat_lang_list");
chrome.storage.sync.get(["nat_lang"], function(result) {
    nat_lang_list.value = result.nat_lang;
});

nat_lang_list.addEventListener(
    "change",
    function() {
        nat_lang = nat_lang_list.options[nat_lang_list.selectedIndex].value;
        console.log(nat_lang);
        set_lang(nat_lang, nat_lang_list);
    },
    false
);
