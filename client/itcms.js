/*
* Author: Oliver Careaga
* Version: beta
* Date: 160513
*/

// ---------------------------------------- Resource functions ----------
/**
* Search and return an object within a list for a particular index.
*
* @param {List} object - List where search. Inits with second parameter on reduce() method.
* @param {string} currentValue - Value to search into list.
* @param {int} i - Current index.
* @param {Array} arr - Initial array.
* @return {List|string|null}
*/
function stringToDotNotation(object, currentValue, i, arr){
	var result = null;
	
	try{
		if(object != null){
			if(currentValue.substr(-1) == ']'){
				result = object[currentValue.slice(0, -3)][currentValue.charAt(currentValue.length - 2)]; // object[arrayName][arrayIndex]
			} else{
				result = object[currentValue];
			}
			
			if(result === undefined){
				throw (i + 1 == arr.length) ? true : false;
			}
		} else{
			throw (i + 1 == arr.length) ? true : false;
		}
	}
	catch(e){
		if(e){ // Latest value
			result = arr.join('.');
			console.log('No result was found for query "' + result + '".');
		} else{
			result = null;
		}
	}
	finally{
		return result;
	}
}

// ---------------------------------------- Objects ----------
/**
* Create an instance of ITCMS.
*
* @constructor
* @this {ITCMS}
* @param {function} callback - Callback function.
*/
function ITCMS(callback){
	var base = this;
	base.callback = callback;
	base.pageObject = null;
	base.wsgiLocation = '/wsgi';
	base.database = 'itcms';
	base.page = document.querySelector('[data-page]').getAttribute('data-page');
	base.language = document.documentElement.lang;
	base.languageSelectors = document.querySelectorAll('[data-language-selector]');
	base.ajaxError = false;
	base.queryDestinations = [
		'placeholder',
		'value'
	];
	
	base.init = function(){
		// Function calls
		base.updateLanguageSelectors();
		
		if(localStorage.language){
			base.changeLanguage(localStorage.language);
		} else{
			localStorage.setItem('language', base.language);
		}
		
		// Event listeners
		for(var i = 0; i < base.languageSelectors.length; i++){
			base.languageSelectors[i].addEventListener('click', function(){
				base.changeLanguage(this.getAttribute('data-language-selector'));
			});
		}
	}
	
	/**
	* Update 'data-language-selector-state' attributes.
	*/
	base.updateLanguageSelectors = function(){
		for(var i = 0; i < base.languageSelectors.length; i++){
			if(base.languageSelectors[i].getAttribute('data-language-selector') == base.language){
				base.languageSelectors[i].setAttribute('data-language-selector-state', true);
			} else{
				base.languageSelectors[i].setAttribute('data-language-selector-state', false);
			}
		}
	}
	
	/**
	* If server returns a page object, call 'changeLanguage()' with him.
	*
	* @param {string} language - Language code.
	* @param {function} overwriteCallback - Overwrite instance's callback function.
	*/
	base.changeLanguage = function(language, overwriteCallback){
		if(language && language != base.language && !base.ajaxError){
			// Hide content while ITCMS is working
			//document.querySelector('body').style.display = 'none';
			
			// W3C recommendation: Instance a new xhr for each AJAX task.
			var xhr = new XMLHttpRequest();
			
			xhr.onreadystatechange = function(){
				if(this.readyState == XMLHttpRequest.DONE){
					if(this.status == 200){
						base.pageObject = JSON.parse(this.responseText);
						if(base.pageObject){
							// New language setters
							base.language = language;
							localStorage.language = language;
							
							// DOM elements replacement
							base.replaceQueries();
							
							// Update language selectors' state
							base.updateLanguageSelectors();
							
							// To callback function
							if(base.callback){
								base.callback(language);
							} else if(overwriteCallback){
								overwriteCallback(language);
							}
						} else{
							console.log('Empty "pageObject" property.');
						}
					} else{
						// If there's a first error, call the function again
						if(this.status == 0 && !base.ajaxError){
							base.ajaxError = true;
							base.changeLanguage(language);
						} else{
							alert('Status ' + this.status + ' returned: ' +  this.statusText);
						}
					}
				}
			}
			
			xhr.open('POST', base.wsgiLocation, true);
			//xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.send('database=' + base.database + '&pageCode=' + base.page + '&languageCode=' + language);
		
		} else{
			if(language){
				console.log('HTML "lang" attribute or selection [' + base.language + 
					'] matches with "localStorage.language" [' + 
					localStorage.language + '].');
			} else{
				console.log('Missing "language" parameter.');
			}
		}
	}
	
	/**
	* Replace 'data-get' by the appropiate value.
	*/
	base.replaceQueries = function(){
		// Simple data-get replacements
		var queryElements = document.querySelectorAll('[data-get]');
		
		for(var i = 0; i < queryElements.length; i++){
			queryElements[i].innerHTML = queryElements[i].getAttribute('data-get').split('.').reduce(stringToDotNotation, base.pageObject);
		}
		
		// Special data-get replacements
		for(var i = 0; i < base.queryDestinations.length; i++){
			var querySpecialElements = document.querySelectorAll('[data-get-' + base.queryDestinations[i] +']');
		
			for(var j = 0; j < querySpecialElements.length; j++){
				querySpecialElements[j].setAttribute(
					base.queryDestinations[i], 
					querySpecialElements[j].getAttribute('data-get-' + base.queryDestinations[i]).split('.').reduce(stringToDotNotation, base.pageObject)
				);
			}
		}
		
		// Show content again
		//document.querySelector('body').removeAttribute('style');
	}
	
	// Init call on instance
	base.init();
}