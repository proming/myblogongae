tinyMCEPopup.requireLangPack();

var SyntaxHLDialog = {
	init : function() {
	},

	insert : function() {
		var f = document.forms[0], textarea_output, options = '';
		
		//If no code just return.
		if(f.syntaxhl_code.value == '') {
			tinyMCEPopup.close();
			return false;
		}
		
		if(f.syntaxhl_nogutter.checked) {
			options += 'gutter: false; ';
		}
		if(f.syntaxhl_light.checked) {
			options += 'light: true; ';
		}
		if(f.syntaxhl_collapse.checked) {
			options += 'collapse: true; ';
		}
		if(f.syntaxhl_fontsize.value != '') {
			var fontsize=parseInt(f.syntaxhl_fontsize.value);
			options += 'fontsize: ' + fontsize + '; ';
		}
		
		if(f.syntaxhl_firstline.value != '') {
			var linenumber = parseInt(f.syntaxhl_firstline.value);
			options += 'first-line: ' + linenumber + '; ';
		}
		if(f.syntaxhl_highlight.value != '') {
			options += 'highlight: [' + f.syntaxhl_highlight.value + ']; ';
		}
		/*escape code's HTML */
		codeText=f.syntaxhl_code.value.replace(/</g,"&lt;");
		codeText.replace(/>/g,"&gt;");
		codeText.replace(/'/g,"&#39;");
		codeText.replace(/"/g,"&quot;");
		codeText.replace(/&/g,"&amp;");
		textarea_output = '<pre class="brush: ';
		textarea_output += f.syntaxhl_language.value + ';' + options + '">';
		textarea_output += codeText;
		textarea_output += '</pre> '; /* note space at the end, had a bug it was inserting twice? */
		tinyMCEPopup.editor.execCommand('mceInsertContent', false, textarea_output);
		tinyMCEPopup.close();
	}
};

tinyMCEPopup.onInit.add(SyntaxHLDialog.init, SyntaxHLDialog);
