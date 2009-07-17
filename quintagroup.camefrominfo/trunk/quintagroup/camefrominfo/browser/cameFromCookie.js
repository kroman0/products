function setCFCookie() {
    var own_domain = document.domain;
    var currRef = document.referrer;
    var cookie_name = "cmfrm";
    var domain = currRef.match(/:\/\/(www\.)?([^\/:]+)/);
    domain = (domain != null && domain[2]) ? domain[2] : '';
    if ((domain.toLowerCase() != own_domain) || (domain == '')) {
        // set cookie with new referrer
        createCookie(cookie_name, currRef);
    }
};

function registerPloneFunction(func) {
    if (window.addEventListener) window.addEventListener("load",func,false);
    else if (window.attachEvent) window.attachEvent("onload",func);   
};

registerPloneFunction(setCFCookie);
