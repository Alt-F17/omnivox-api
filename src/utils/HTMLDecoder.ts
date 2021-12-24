export function decodeHTMLEntities (str: string) {
    if(str && typeof str === 'string') {
      //str = str.replace(/<script[^>]*>([\S\s]*?)<\/script>/gmi, '');
      str = str.replace(/<\/?\w(?:[^"'>]|"[^"]*"|'[^']*')*>/gmi, '');
    }

    return str;
}

export function decodeHTMLCharCodes(str: string) { 
    str = str.replace(/(&#(\d+);)/g, (_, __, charCode) => {
        return String.fromCharCode(charCode);
    });

    str = str.replace(new RegExp("&quot;", "gm"), '\"');

    const nbspReg = new RegExp("&nbsp;", "g");
    str = str.replace(nbspReg, " ");

  return str;
}
