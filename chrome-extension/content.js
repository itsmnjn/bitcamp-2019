function getSelectionHtml() {
    var html = "";
    var sel = "";
    if (typeof window.getSelection != "undefined") {
        sel = window.getSelection();
        if (sel.rangeCount) {
            var container = document.createElement("div");
            for (var i = 0, len = sel.rangeCount; i < len; ++i) {
                container.appendChild(sel.getRangeAt(i).cloneContents());
            }
            html = container.innerHTML;
        }
    } else if (typeof document.selection != "undefined") {
        if (document.selection.type == "Text") {
            sel = document.selection;
            html = document.selection.createRange().htmlText;
        }
    }
    return { selection: sel, html: html };
}

function sendSentence() {
    var sentences = [];
    var sentence = "";
    var selection = window.getSelection();
    var selection_text = selection.toString();
    var parentNode = selection.anchorNode.parentNode;
    $(parentNode).each(function() {
        $(this).html(
            $(this)
                .text()
                .split(/([\.\?!])(?= )/)
                .map(function(v) {
                    sentences.push(v);
                    return "<span class=sentence>" + v + "</span>";
                })
        );
    });
    var i = 0;
    while (sentences[i].indexOf(selection_text) == -1) {
        i++;
    }
    sentence = sentences[i];
    chrome.runtime.sendMessage({ sentence: sentence }, function(response) {
        console.log(response.farewell);
    });
}
