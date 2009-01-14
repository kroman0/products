function adjustIFrameSize (iframeWindow) {
    if (iframeWindow.document.height) {
        var iframeElement = document.getElementById(iframeWindow.name);
        iframeElement.style.height = iframeWindow.document.height + 20 +'px';
//        iframeElement.style.width = iframeWindow.document.width + 20 + 'px';
    } else if (document.all) {
        var iframeElement = document.all[iframeWindow.name];
        if (iframeWindow.document.compatMode && iframeWindow.document.compatMode != 'BackCompat') {
            iframeElement.style.height = iframeWindow.document.documentElement.scrollHeight + 20 + 'px';
//            iframeElement.style.width = iframeWindow.document.documentElement.scrollWidth + 20 + 'px';
        } else {
            iframeElement.style.height = iframeWindow.document.body.scrollHeight + 20 + 'px';
//            iframeElement.style.width = iframeWindow.document.body.scrollWidth + 20 + 'px';
        }
    }
}