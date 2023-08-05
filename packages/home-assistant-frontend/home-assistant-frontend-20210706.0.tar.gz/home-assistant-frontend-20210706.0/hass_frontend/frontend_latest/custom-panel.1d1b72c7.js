/*! For license information please see custom-panel.1d1b72c7.js.LICENSE.txt */
(()=>{var e,t,r={25945:(e,t,r)=>{"use strict";r.d(t,{fl:()=>g,iv:()=>l});const o=window.ShadowRoot&&(void 0===window.ShadyCSS||window.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,i=Symbol();class a{constructor(e,t){if(t!==i)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e}get styleSheet(){return o&&void 0===this.t&&(this.t=new CSSStyleSheet,this.t.replaceSync(this.cssText)),this.t}toString(){return this.cssText}}const n=new Map,s=e=>{let t=n.get(e);return void 0===t&&n.set(e,t=new a(e,i)),t},l=(e,...t)=>{const r=1===e.length?e[0]:t.reduce(((t,r,o)=>t+(e=>{if(e instanceof a)return e.cssText;if("number"==typeof e)return e;throw Error("Value passed to 'css' function must be a 'css' function result: "+e+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(r)+e[o+1]),e[0]);return s(r)},c=(e,t)=>{o?e.adoptedStyleSheets=t.map((e=>e instanceof CSSStyleSheet?e:e.styleSheet)):t.forEach((t=>{const r=document.createElement("style");r.textContent=t.cssText,e.appendChild(r)}))},d=o?e=>e:e=>e instanceof CSSStyleSheet?(e=>{let t="";for(const r of e.cssRules)t+=r.cssText;return(e=>s("string"==typeof e?e:e+""))(t)})(e):e;var h,p,u,v;const m={toAttribute(e,t){switch(t){case Boolean:e=e?"":null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let r=e;switch(t){case Boolean:r=null!==e;break;case Number:r=null===e?null:Number(e);break;case Object:case Array:try{r=JSON.parse(e)}catch(e){r=null}}return r}},f=(e,t)=>t!==e&&(t==t||e==e),b={attribute:!0,type:String,converter:m,reflect:!1,hasChanged:f};class g extends HTMLElement{constructor(){super(),this.Πi=new Map,this.Πo=void 0,this.Πl=void 0,this.isUpdatePending=!1,this.hasUpdated=!1,this.Πh=null,this.u()}static addInitializer(e){var t;null!==(t=this.v)&&void 0!==t||(this.v=[]),this.v.push(e)}static get observedAttributes(){this.finalize();const e=[];return this.elementProperties.forEach(((t,r)=>{const o=this.Πp(r,t);void 0!==o&&(this.Πm.set(o,r),e.push(o))})),e}static createProperty(e,t=b){if(t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),!t.noAccessor&&!this.prototype.hasOwnProperty(e)){const r="symbol"==typeof e?Symbol():"__"+e,o=this.getPropertyDescriptor(e,r,t);void 0!==o&&Object.defineProperty(this.prototype,e,o)}}static getPropertyDescriptor(e,t,r){return{get(){return this[t]},set(o){const i=this[e];this[t]=o,this.requestUpdate(e,i,r)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||b}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),this.elementProperties=new Map(e.elementProperties),this.Πm=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const r of t)this.createProperty(r,e[r])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){const t=[];if(Array.isArray(e)){const r=new Set(e.flat(1/0).reverse());for(const e of r)t.unshift(d(e))}else void 0!==e&&t.push(d(e));return t}static Πp(e,t){const r=t.attribute;return!1===r?void 0:"string"==typeof r?r:"string"==typeof e?e.toLowerCase():void 0}u(){var e;this.Πg=new Promise((e=>this.enableUpdating=e)),this.L=new Map,this.Π_(),this.requestUpdate(),null===(e=this.constructor.v)||void 0===e||e.forEach((e=>e(this)))}addController(e){var t,r;(null!==(t=this.ΠU)&&void 0!==t?t:this.ΠU=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&(null===(r=e.hostConnected)||void 0===r||r.call(e))}removeController(e){var t;null===(t=this.ΠU)||void 0===t||t.splice(this.ΠU.indexOf(e)>>>0,1)}Π_(){this.constructor.elementProperties.forEach(((e,t)=>{this.hasOwnProperty(t)&&(this.Πi.set(t,this[t]),delete this[t])}))}createRenderRoot(){var e;const t=null!==(e=this.shadowRoot)&&void 0!==e?e:this.attachShadow(this.constructor.shadowRootOptions);return c(t,this.constructor.elementStyles),t}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostConnected)||void 0===t?void 0:t.call(e)})),this.Πl&&(this.Πl(),this.Πo=this.Πl=void 0)}enableUpdating(e){}disconnectedCallback(){var e;null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostDisconnected)||void 0===t?void 0:t.call(e)})),this.Πo=new Promise((e=>this.Πl=e))}attributeChangedCallback(e,t,r){this.K(e,r)}Πj(e,t,r=b){var o,i;const a=this.constructor.Πp(e,r);if(void 0!==a&&!0===r.reflect){const n=(null!==(i=null===(o=r.converter)||void 0===o?void 0:o.toAttribute)&&void 0!==i?i:m.toAttribute)(t,r.type);this.Πh=e,null==n?this.removeAttribute(a):this.setAttribute(a,n),this.Πh=null}}K(e,t){var r,o,i;const a=this.constructor,n=a.Πm.get(e);if(void 0!==n&&this.Πh!==n){const e=a.getPropertyOptions(n),s=e.converter,l=null!==(i=null!==(o=null===(r=s)||void 0===r?void 0:r.fromAttribute)&&void 0!==o?o:"function"==typeof s?s:null)&&void 0!==i?i:m.fromAttribute;this.Πh=n,this[n]=l(t,e.type),this.Πh=null}}requestUpdate(e,t,r){let o=!0;void 0!==e&&(((r=r||this.constructor.getPropertyOptions(e)).hasChanged||f)(this[e],t)?(this.L.has(e)||this.L.set(e,t),!0===r.reflect&&this.Πh!==e&&(void 0===this.Πk&&(this.Πk=new Map),this.Πk.set(e,r))):o=!1),!this.isUpdatePending&&o&&(this.Πg=this.Πq())}async Πq(){this.isUpdatePending=!0;try{for(await this.Πg;this.Πo;)await this.Πo}catch(e){Promise.reject(e)}const e=this.performUpdate();return null!=e&&await e,!this.isUpdatePending}performUpdate(){var e;if(!this.isUpdatePending)return;this.hasUpdated,this.Πi&&(this.Πi.forEach(((e,t)=>this[t]=e)),this.Πi=void 0);let t=!1;const r=this.L;try{t=this.shouldUpdate(r),t?(this.willUpdate(r),null===(e=this.ΠU)||void 0===e||e.forEach((e=>{var t;return null===(t=e.hostUpdate)||void 0===t?void 0:t.call(e)})),this.update(r)):this.Π$()}catch(e){throw t=!1,this.Π$(),e}t&&this.E(r)}willUpdate(e){}E(e){var t;null===(t=this.ΠU)||void 0===t||t.forEach((e=>{var t;return null===(t=e.hostUpdated)||void 0===t?void 0:t.call(e)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}Π$(){this.L=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this.Πg}shouldUpdate(e){return!0}update(e){void 0!==this.Πk&&(this.Πk.forEach(((e,t)=>this.Πj(t,this[t],e))),this.Πk=void 0),this.Π$()}updated(e){}firstUpdated(e){}}g.finalized=!0,g.elementProperties=new Map,g.elementStyles=[],g.shadowRootOptions={mode:"open"},null===(p=(h=globalThis).reactiveElementPlatformSupport)||void 0===p||p.call(h,{ReactiveElement:g}),(null!==(u=(v=globalThis).reactiveElementVersions)&&void 0!==u?u:v.reactiveElementVersions=[]).push("1.0.0-rc.2")},29561:(e,t,r)=>{"use strict";r.d(t,{iv:()=>c.iv,dy:()=>d.dy,YP:()=>d.YP,oi:()=>h});var o,i,a,n,s,l,c=r(25945),d=r(99602);(null!==(o=(l=globalThis).litElementVersions)&&void 0!==o?o:l.litElementVersions=[]).push("3.0.0-rc.2");class h extends c.fl{constructor(){super(...arguments),this.renderOptions={host:this},this.Φt=void 0}createRenderRoot(){var e,t;const r=super.createRenderRoot();return null!==(e=(t=this.renderOptions).renderBefore)&&void 0!==e||(t.renderBefore=r.firstChild),r}update(e){const t=this.render();super.update(e),this.Φt=(0,d.sY)(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null===(e=this.Φt)||void 0===e||e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.Φt)||void 0===e||e.setConnected(!1)}render(){return d.Jb}}h.finalized=!0,h._$litElement$=!0,null===(a=(i=globalThis).litElementHydrateSupport)||void 0===a||a.call(i,{LitElement:h}),null===(s=(n=globalThis).litElementPlatformSupport)||void 0===s||s.call(n,{LitElement:h})},99602:(e,t,r)=>{"use strict";var o,i,a,n;r.d(t,{dy:()=>E,Jb:()=>C,sY:()=>U,YP:()=>P});const s=globalThis.trustedTypes,l=s?s.createPolicy("lit-html",{createHTML:e=>e}):void 0,c=`lit$${(Math.random()+"").slice(9)}$`,d="?"+c,h=`<${d}>`,p=document,u=(e="")=>p.createComment(e),v=e=>null===e||"object"!=typeof e&&"function"!=typeof e,m=Array.isArray,f=e=>{var t;return m(e)||"function"==typeof(null===(t=e)||void 0===t?void 0:t[Symbol.iterator])},b=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,g=/-->/g,y=/>/g,w=/>|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,x=/'/g,k=/"/g,_=/^(?:script|style|textarea)$/i,S=e=>(t,...r)=>({_$litType$:e,strings:t,values:r}),E=S(1),P=S(2),C=Symbol.for("lit-noChange"),A=Symbol.for("lit-nothing"),$=new WeakMap,U=(e,t,r)=>{var o,i;const a=null!==(o=null==r?void 0:r.renderBefore)&&void 0!==o?o:t;let n=a._$litPart$;if(void 0===n){const e=null!==(i=null==r?void 0:r.renderBefore)&&void 0!==i?i:null;a._$litPart$=n=new B(t.insertBefore(u(),e),e,void 0,r)}return n.I(e),n},T=p.createTreeWalker(p,129,null,!1),O=(e,t)=>{const r=e.length-1,o=[];let i,a=2===t?"<svg>":"",n=b;for(let t=0;t<r;t++){const r=e[t];let s,l,d=-1,p=0;for(;p<r.length&&(n.lastIndex=p,l=n.exec(r),null!==l);)p=n.lastIndex,n===b?"!--"===l[1]?n=g:void 0!==l[1]?n=y:void 0!==l[2]?(_.test(l[2])&&(i=RegExp("</"+l[2],"g")),n=w):void 0!==l[3]&&(n=w):n===w?">"===l[0]?(n=null!=i?i:b,d=-1):void 0===l[1]?d=-2:(d=n.lastIndex-l[2].length,s=l[1],n=void 0===l[3]?w:'"'===l[3]?k:x):n===k||n===x?n=w:n===g||n===y?n=b:(n=w,i=void 0);const u=n===w&&e[t+1].startsWith("/>")?" ":"";a+=n===b?r+h:d>=0?(o.push(s),r.slice(0,d)+"$lit$"+r.slice(d)+c+u):r+c+(-2===d?(o.push(void 0),t):u)}const s=a+(e[r]||"<?>")+(2===t?"</svg>":"");return[void 0!==l?l.createHTML(s):s,o]};class H{constructor({strings:e,_$litType$:t},r){let o;this.parts=[];let i=0,a=0;const n=e.length-1,l=this.parts,[h,p]=O(e,t);if(this.el=H.createElement(h,r),T.currentNode=this.el.content,2===t){const e=this.el.content,t=e.firstChild;t.remove(),e.append(...t.childNodes)}for(;null!==(o=T.nextNode())&&l.length<n;){if(1===o.nodeType){if(o.hasAttributes()){const e=[];for(const t of o.getAttributeNames())if(t.endsWith("$lit$")||t.startsWith(c)){const r=p[a++];if(e.push(t),void 0!==r){const e=o.getAttribute(r.toLowerCase()+"$lit$").split(c),t=/([.?@])?(.*)/.exec(r);l.push({type:1,index:i,name:t[2],strings:e,ctor:"."===t[1]?L:"?"===t[1]?z:"@"===t[1]?M:R})}else l.push({type:6,index:i})}for(const t of e)o.removeAttribute(t)}if(_.test(o.tagName)){const e=o.textContent.split(c),t=e.length-1;if(t>0){o.textContent=s?s.emptyScript:"";for(let r=0;r<t;r++)o.append(e[r],u()),T.nextNode(),l.push({type:2,index:++i});o.append(e[t],u())}}}else if(8===o.nodeType)if(o.data===d)l.push({type:2,index:i});else{let e=-1;for(;-1!==(e=o.data.indexOf(c,e+1));)l.push({type:7,index:i}),e+=c.length-1}i++}}static createElement(e,t){const r=p.createElement("template");return r.innerHTML=e,r}}function N(e,t,r=e,o){var i,a,n,s;if(t===C)return t;let l=void 0!==o?null===(i=r.Σi)||void 0===i?void 0:i[o]:r.Σo;const c=v(t)?void 0:t._$litDirective$;return(null==l?void 0:l.constructor)!==c&&(null===(a=null==l?void 0:l.O)||void 0===a||a.call(l,!1),void 0===c?l=void 0:(l=new c(e),l.T(e,r,o)),void 0!==o?(null!==(n=(s=r).Σi)&&void 0!==n?n:s.Σi=[])[o]=l:r.Σo=l),void 0!==l&&(t=N(e,l.S(e,t.values),l,o)),t}class j{constructor(e,t){this.l=[],this.N=void 0,this.D=e,this.M=t}u(e){var t;const{el:{content:r},parts:o}=this.D,i=(null!==(t=null==e?void 0:e.creationScope)&&void 0!==t?t:p).importNode(r,!0);T.currentNode=i;let a=T.nextNode(),n=0,s=0,l=o[0];for(;void 0!==l;){if(n===l.index){let t;2===l.type?t=new B(a,a.nextSibling,this,e):1===l.type?t=new l.ctor(a,l.name,l.strings,this,e):6===l.type&&(t=new F(a,this,e)),this.l.push(t),l=o[++s]}n!==(null==l?void 0:l.index)&&(a=T.nextNode(),n++)}return i}v(e){let t=0;for(const r of this.l)void 0!==r&&(void 0!==r.strings?(r.I(e,r,t),t+=r.strings.length-2):r.I(e[t])),t++}}class B{constructor(e,t,r,o){this.type=2,this.N=void 0,this.A=e,this.B=t,this.M=r,this.options=o}setConnected(e){var t;null===(t=this.P)||void 0===t||t.call(this,e)}get parentNode(){return this.A.parentNode}get startNode(){return this.A}get endNode(){return this.B}I(e,t=this){e=N(this,e,t),v(e)?e===A||null==e||""===e?(this.H!==A&&this.R(),this.H=A):e!==this.H&&e!==C&&this.m(e):void 0!==e._$litType$?this._(e):void 0!==e.nodeType?this.$(e):f(e)?this.g(e):this.m(e)}k(e,t=this.B){return this.A.parentNode.insertBefore(e,t)}$(e){this.H!==e&&(this.R(),this.H=this.k(e))}m(e){const t=this.A.nextSibling;null!==t&&3===t.nodeType&&(null===this.B?null===t.nextSibling:t===this.B.previousSibling)?t.data=e:this.$(p.createTextNode(e)),this.H=e}_(e){var t;const{values:r,_$litType$:o}=e,i="number"==typeof o?this.C(e):(void 0===o.el&&(o.el=H.createElement(o.h,this.options)),o);if((null===(t=this.H)||void 0===t?void 0:t.D)===i)this.H.v(r);else{const e=new j(i,this),t=e.u(this.options);e.v(r),this.$(t),this.H=e}}C(e){let t=$.get(e.strings);return void 0===t&&$.set(e.strings,t=new H(e)),t}g(e){m(this.H)||(this.H=[],this.R());const t=this.H;let r,o=0;for(const i of e)o===t.length?t.push(r=new B(this.k(u()),this.k(u()),this,this.options)):r=t[o],r.I(i),o++;o<t.length&&(this.R(r&&r.B.nextSibling,o),t.length=o)}R(e=this.A.nextSibling,t){var r;for(null===(r=this.P)||void 0===r||r.call(this,!1,!0,t);e&&e!==this.B;){const t=e.nextSibling;e.remove(),e=t}}}class R{constructor(e,t,r,o,i){this.type=1,this.H=A,this.N=void 0,this.V=void 0,this.element=e,this.name=t,this.M=o,this.options=i,r.length>2||""!==r[0]||""!==r[1]?(this.H=Array(r.length-1).fill(A),this.strings=r):this.H=A}get tagName(){return this.element.tagName}I(e,t=this,r,o){const i=this.strings;let a=!1;if(void 0===i)e=N(this,e,t,0),a=!v(e)||e!==this.H&&e!==C,a&&(this.H=e);else{const o=e;let n,s;for(e=i[0],n=0;n<i.length-1;n++)s=N(this,o[r+n],t,n),s===C&&(s=this.H[n]),a||(a=!v(s)||s!==this.H[n]),s===A?e=A:e!==A&&(e+=(null!=s?s:"")+i[n+1]),this.H[n]=s}a&&!o&&this.W(e)}W(e){e===A?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class L extends R{constructor(){super(...arguments),this.type=3}W(e){this.element[this.name]=e===A?void 0:e}}class z extends R{constructor(){super(...arguments),this.type=4}W(e){e&&e!==A?this.element.setAttribute(this.name,""):this.element.removeAttribute(this.name)}}class M extends R{constructor(){super(...arguments),this.type=5}I(e,t=this){var r;if((e=null!==(r=N(this,e,t,0))&&void 0!==r?r:A)===C)return;const o=this.H,i=e===A&&o!==A||e.capture!==o.capture||e.once!==o.once||e.passive!==o.passive,a=e!==A&&(o===A||i);i&&this.element.removeEventListener(this.name,this,o),a&&this.element.addEventListener(this.name,this,e),this.H=e}handleEvent(e){var t,r;"function"==typeof this.H?this.H.call(null!==(r=null===(t=this.options)||void 0===t?void 0:t.host)&&void 0!==r?r:this.element,e):this.H.handleEvent(e)}}class F{constructor(e,t,r){this.element=e,this.type=6,this.N=void 0,this.V=void 0,this.M=t,this.options=r}I(e){N(this,e)}}null===(i=(o=globalThis).litHtmlPlatformSupport)||void 0===i||i.call(o,H,B),(null!==(a=(n=globalThis).litHtmlVersions)&&void 0!==a?a:n.litHtmlVersions=[]).push("2.0.0-rc.3")},50424:(e,t,r)=>{"use strict";r.d(t,{oi:()=>o.oi,iv:()=>o.iv,dy:()=>o.dy,YP:()=>o.YP});r(25945),r(99602);var o=r(29561)},47181:(e,t,r)=>{"use strict";r.d(t,{B:()=>o});const o=(e,t,r,o)=>{o=o||{},r=null==r?{}:r;const i=new Event(t,{bubbles:void 0===o.bubbles||o.bubbles,cancelable:Boolean(o.cancelable),composed:void 0===o.composed||o.composed});return i.detail=r,e.dispatchEvent(i),i}},37846:()=>{if(/^((?!chrome|android).)*version\/14\.0\s.*safari/i.test(navigator.userAgent)){const e=window.Element.prototype.attachShadow;window.Element.prototype.attachShadow=function(t){return t&&t.delegatesFocus&&delete t.delegatesFocus,e.apply(this,[t])}}},11654:(e,t,r)=>{"use strict";r.d(t,{_l:()=>i,q0:()=>a,Qx:()=>s,e$:()=>l});var o=r(50424);const i={"primary-background-color":"#111111","card-background-color":"#1c1c1c","secondary-background-color":"#202020","primary-text-color":"#e1e1e1","secondary-text-color":"#9b9b9b","disabled-text-color":"#6f6f6f","app-header-text-color":"#e1e1e1","app-header-background-color":"#101e24","switch-unchecked-button-color":"#999999","switch-unchecked-track-color":"#9b9b9b","divider-color":"rgba(225, 225, 225, .12)","mdc-ripple-color":"#AAAAAA","codemirror-keyword":"#C792EA","codemirror-operator":"#89DDFF","codemirror-variable":"#f07178","codemirror-variable-2":"#EEFFFF","codemirror-variable-3":"#DECB6B","codemirror-builtin":"#FFCB6B","codemirror-atom":"#F78C6C","codemirror-number":"#FF5370","codemirror-def":"#82AAFF","codemirror-string":"#C3E88D","codemirror-string-2":"#f07178","codemirror-comment":"#545454","codemirror-tag":"#FF5370","codemirror-meta":"#FFCB6B","codemirror-attribute":"#C792EA","codemirror-property":"#C792EA","codemirror-qualifier":"#DECB6B","codemirror-type":"#DECB6B"},a={"state-icon-error-color":"var(--error-state-color, var(--error-color))","state-unavailable-color":"var(--state-icon-unavailable-color, var(--disabled-text-color))","sidebar-text-color":"var(--primary-text-color)","sidebar-background-color":"var(--card-background-color)","sidebar-selected-text-color":"var(--primary-color)","sidebar-selected-icon-color":"var(--primary-color)","sidebar-icon-color":"rgba(var(--rgb-primary-text-color), 0.6)","switch-checked-color":"var(--primary-color)","switch-checked-button-color":"var(--switch-checked-color, var(--primary-background-color))","switch-checked-track-color":"var(--switch-checked-color, #000000)","switch-unchecked-button-color":"var(--switch-unchecked-color, var(--primary-background-color))","switch-unchecked-track-color":"var(--switch-unchecked-color, #000000)","slider-color":"var(--primary-color)","slider-secondary-color":"var(--light-primary-color)","slider-bar-color":"var(--disabled-text-color)","label-badge-grey":"var(--paper-grey-500)","label-badge-background-color":"var(--card-background-color)","label-badge-text-color":"rgba(var(--rgb-primary-text-color), 0.8)","paper-listbox-background-color":"var(--card-background-color)","paper-item-icon-color":"var(--state-icon-color)","paper-item-icon-active-color":"var(--state-icon-active-color)","table-row-background-color":"var(--primary-background-color)","table-row-alternative-background-color":"var(--secondary-background-color)","paper-slider-knob-color":"var(--slider-color)","paper-slider-knob-start-color":"var(--slider-color)","paper-slider-pin-color":"var(--slider-color)","paper-slider-pin-start-color":"var(--slider-color)","paper-slider-active-color":"var(--slider-color)","paper-slider-secondary-color":"var(--slider-secondary-color)","paper-slider-container-color":"var(--slider-bar-color)","data-table-background-color":"var(--card-background-color)","markdown-code-background-color":"var(--primary-background-color)","mdc-theme-primary":"var(--primary-color)","mdc-theme-secondary":"var(--accent-color)","mdc-theme-background":"var(--primary-background-color)","mdc-theme-surface":"var(--card-background-color)","mdc-theme-on-primary":"var(--text-primary-color)","mdc-theme-on-secondary":"var(--text-primary-color)","mdc-theme-on-surface":"var(--primary-text-color)","mdc-theme-text-disabled-on-light":"var(--disabled-text-color)","mdc-theme-text-primary-on-background":"var(--primary-text-color)","mdc-theme-text-secondary-on-background":"var(--secondary-text-color)","mdc-theme-text-icon-on-background":"var(--secondary-text-color)","app-header-text-color":"var(--text-primary-color)","app-header-background-color":"var(--primary-color)","material-body-text-color":"var(--primary-text-color)","material-background-color":"var(--card-background-color)","material-secondary-background-color":"var(--secondary-background-color)","material-secondary-text-color":"var(--secondary-text-color)","mdc-checkbox-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-checkbox-disabled-color":"var(--disabled-text-color)","mdc-radio-unchecked-color":"rgba(var(--rgb-primary-text-color), 0.54)","mdc-radio-disabled-color":"var(--disabled-text-color)","mdc-tab-text-label-color-default":"var(--primary-text-color)","mdc-button-disabled-ink-color":"var(--disabled-text-color)","mdc-button-outline-color":"var(--divider-color)","mdc-dialog-scroll-divider-color":"var(--divider-color)","chip-background-color":"rgba(var(--rgb-primary-text-color), 0.15)"},n=o.iv`
  button.link {
    background: none;
    color: inherit;
    border: none;
    padding: 0;
    font: inherit;
    text-align: left;
    text-decoration: underline;
    cursor: pointer;
  }
`,s=o.iv`
  :host {
    font-family: var(--paper-font-body1_-_font-family);
    -webkit-font-smoothing: var(--paper-font-body1_-_-webkit-font-smoothing);
    font-size: var(--paper-font-body1_-_font-size);
    font-weight: var(--paper-font-body1_-_font-weight);
    line-height: var(--paper-font-body1_-_line-height);
  }

  app-header-layout,
  ha-app-layout {
    background-color: var(--primary-background-color);
  }

  app-header,
  app-toolbar {
    background-color: var(--app-header-background-color);
    font-weight: 400;
    color: var(--app-header-text-color, white);
  }

  app-toolbar {
    height: var(--header-height);
  }

  app-header div[sticky] {
    height: 48px;
  }

  app-toolbar [main-title] {
    margin-left: 20px;
  }

  h1 {
    font-family: var(--paper-font-headline_-_font-family);
    -webkit-font-smoothing: var(--paper-font-headline_-_-webkit-font-smoothing);
    white-space: var(--paper-font-headline_-_white-space);
    overflow: var(--paper-font-headline_-_overflow);
    text-overflow: var(--paper-font-headline_-_text-overflow);
    font-size: var(--paper-font-headline_-_font-size);
    font-weight: var(--paper-font-headline_-_font-weight);
    line-height: var(--paper-font-headline_-_line-height);
  }

  h2 {
    font-family: var(--paper-font-title_-_font-family);
    -webkit-font-smoothing: var(--paper-font-title_-_-webkit-font-smoothing);
    white-space: var(--paper-font-title_-_white-space);
    overflow: var(--paper-font-title_-_overflow);
    text-overflow: var(--paper-font-title_-_text-overflow);
    font-size: var(--paper-font-title_-_font-size);
    font-weight: var(--paper-font-title_-_font-weight);
    line-height: var(--paper-font-title_-_line-height);
  }

  h3 {
    font-family: var(--paper-font-subhead_-_font-family);
    -webkit-font-smoothing: var(--paper-font-subhead_-_-webkit-font-smoothing);
    white-space: var(--paper-font-subhead_-_white-space);
    overflow: var(--paper-font-subhead_-_overflow);
    text-overflow: var(--paper-font-subhead_-_text-overflow);
    font-size: var(--paper-font-subhead_-_font-size);
    font-weight: var(--paper-font-subhead_-_font-weight);
    line-height: var(--paper-font-subhead_-_line-height);
  }

  a {
    color: var(--primary-color);
  }

  .secondary {
    color: var(--secondary-text-color);
  }

  .error {
    color: var(--error-color);
  }

  .warning {
    color: var(--error-color);
  }

  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }

  ${n}

  .card-actions a {
    text-decoration: none;
  }

  .card-actions .warning {
    --mdc-theme-primary: var(--error-color);
  }

  .layout.horizontal,
  .layout.vertical {
    display: flex;
  }
  .layout.inline {
    display: inline-flex;
  }
  .layout.horizontal {
    flex-direction: row;
  }
  .layout.vertical {
    flex-direction: column;
  }
  .layout.wrap {
    flex-wrap: wrap;
  }
  .layout.no-wrap {
    flex-wrap: nowrap;
  }
  .layout.center,
  .layout.center-center {
    align-items: center;
  }
  .layout.bottom {
    align-items: flex-end;
  }
  .layout.center-justified,
  .layout.center-center {
    justify-content: center;
  }
  .flex {
    flex: 1;
    flex-basis: 0.000000001px;
  }
  .flex-auto {
    flex: 1 1 auto;
  }
  .flex-none {
    flex: none;
  }
  .layout.justified {
    justify-content: space-between;
  }
`,l=(o.iv`
  /* prevent clipping of positioned elements */
  paper-dialog-scrollable {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: auto;
    }
  }

  /* force smooth scrolling for iOS 10 */
  paper-dialog-scrollable.can-scroll {
    --paper-dialog-scrollable: {
      -webkit-overflow-scrolling: touch;
    }
  }

  .paper-dialog-buttons {
    align-items: flex-end;
    padding: 8px;
    padding-bottom: max(env(safe-area-inset-bottom), 8px);
  }

  @media all and (min-width: 450px) and (min-height: 500px) {
    ha-paper-dialog {
      min-width: 400px;
    }
  }

  @media all and (max-width: 450px), all and (max-height: 500px) {
    paper-dialog,
    ha-paper-dialog {
      margin: 0;
      width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      min-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-width: calc(
        100% - env(safe-area-inset-right) - env(safe-area-inset-left)
      ) !important;
      max-height: calc(100% - var(--header-height));

      position: fixed !important;
      bottom: 0px;
      left: env(safe-area-inset-left);
      right: env(safe-area-inset-right);
      overflow: scroll;
      border-bottom-left-radius: 0px;
      border-bottom-right-radius: 0px;
    }
  }

  /* mwc-dialog (ha-dialog) styles */
  ha-dialog {
    --mdc-dialog-min-width: 400px;
    --mdc-dialog-max-width: 600px;
    --mdc-dialog-heading-ink-color: var(--primary-text-color);
    --mdc-dialog-content-ink-color: var(--primary-text-color);
    --justify-action-buttons: space-between;
  }

  ha-dialog .form {
    padding-bottom: 24px;
    color: var(--primary-text-color);
  }

  a {
    color: var(--primary-color);
  }

  /* make dialog fullscreen on small screens */
  @media all and (max-width: 450px), all and (max-height: 500px) {
    ha-dialog {
      --mdc-dialog-min-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-max-width: calc(
        100vw - env(safe-area-inset-right) - env(safe-area-inset-left)
      );
      --mdc-dialog-min-height: 100%;
      --mdc-dialog-max-height: 100%;
      --mdc-shape-medium: 0px;
      --vertial-align-dialog: flex-end;
    }
  }
  mwc-button.warning {
    --mdc-theme-primary: var(--error-color);
  }
  .error {
    color: var(--error-color);
  }
`,o.iv`
  .ha-scrollbar::-webkit-scrollbar {
    width: 0.4rem;
    height: 0.4rem;
  }

  .ha-scrollbar::-webkit-scrollbar-thumb {
    -webkit-border-radius: 4px;
    border-radius: 4px;
    background: var(--scrollbar-thumb-color);
  }

  .ha-scrollbar {
    overflow-y: auto;
    scrollbar-color: var(--scrollbar-thumb-color) transparent;
    scrollbar-width: thin;
  }
`,o.iv`
  body {
    background-color: var(--primary-background-color);
    color: var(--primary-text-color);
    height: calc(100vh - 32px);
    width: 100vw;
  }
`)}},o={};function i(e){if(o[e])return o[e].exports;var t=o[e]={exports:{}};return r[e](t,t.exports,i),t.exports}i.m=r,i.d=(e,t)=>{for(var r in t)i.o(t,r)&&!i.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:t[r]})},i.f={},i.e=e=>Promise.all(Object.keys(i.f).reduce(((t,r)=>(i.f[r](e,t),t)),[])),i.u=e=>"chunk."+{145:"7fa08b14cbed4f042d2b",149:"76c8b4cecec0a2f150be",1479:"86fb31b632f8a9052fd9",2024:"363fcd5ad7790a781e2e",2678:"efc7906c2a15d648c41a",6134:"55732089ac51bda555df",9849:"403a03c45ab57c43ebeb"}[e]+".js",i.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="home-assistant-frontend:",i.l=(r,o,a,n)=>{if(e[r])e[r].push(o);else{var s,l;if(void 0!==a)for(var c=document.getElementsByTagName("script"),d=0;d<c.length;d++){var h=c[d];if(h.getAttribute("src")==r||h.getAttribute("data-webpack")==t+a){s=h;break}}s||(l=!0,(s=document.createElement("script")).charset="utf-8",s.timeout=120,i.nc&&s.setAttribute("nonce",i.nc),s.setAttribute("data-webpack",t+a),s.src=r),e[r]=[o];var p=(t,o)=>{s.onerror=s.onload=null,clearTimeout(u);var i=e[r];if(delete e[r],s.parentNode&&s.parentNode.removeChild(s),i&&i.forEach((e=>e(o))),t)return t(o)},u=setTimeout(p.bind(null,void 0,{type:"timeout",target:s}),12e4);s.onerror=p.bind(null,s.onerror),s.onload=p.bind(null,s.onload),l&&document.head.appendChild(s)}},i.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},i.p="/frontend_latest/",(()=>{var e={8017:0};i.f.j=(t,r)=>{var o=i.o(e,t)?e[t]:void 0;if(0!==o)if(o)r.push(o[2]);else{var a=new Promise(((r,i)=>{o=e[t]=[r,i]}));r.push(o[2]=a);var n=i.p+i.u(t),s=new Error;i.l(n,(r=>{if(i.o(e,t)&&(0!==(o=e[t])&&(e[t]=void 0),o)){var a=r&&("load"===r.type?"missing":r.type),n=r&&r.target&&r.target.src;s.message="Loading chunk "+t+" failed.\n("+a+": "+n+")",s.name="ChunkLoadError",s.type=a,s.request=n,o[1](s)}}),"chunk-"+t,t)}};var t=(t,r)=>{for(var o,a,[n,s,l]=r,c=0,d=[];c<n.length;c++)a=n[c],i.o(e,a)&&e[a]&&d.push(e[a][0]),e[a]=0;for(o in s)i.o(s,o)&&(i.m[o]=s[o]);for(l&&l(i),t&&t(r);d.length;)d.shift()()},r=self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[];r.forEach(t.bind(null,0)),r.push=t.bind(null,r.push.bind(r))})(),(()=>{"use strict";i(37846);var e=i(47181);const t=(e,t,r)=>new Promise(((o,i)=>{const a=document.createElement(e);let n="src",s="body";switch(a.onload=()=>o(t),a.onerror=()=>i(t),e){case"script":a.async=!0,r&&(a.type=r);break;case"link":a.type="text/css",a.rel="stylesheet",n="href",s="head"}a[n]=t,document[s].appendChild(a)})),r=e=>t("script",e),o="customElements"in window&&"content"in document.createElement("template"),a="ha-main-window",n=window.name===a?window:parent.name===a?parent:top;var s=i(11654);const l={},c=e=>{const o=(e=>e.html_url?{type:"html",url:e.html_url}:e.module_url&&e.js_url||e.module_url?{type:"module",url:e.module_url}:{type:"js",url:e.js_url})(e);return"js"===o.type?(o.url in l||(l[o.url]=r(o.url)),l[o.url]):"module"===o.type?(i=o.url,t("script",i,"module")):Promise.reject("No valid url found in panel config.");var i};let d,h;function p(e){h&&((e,t)=>{"setProperties"in e?e.setProperties(t):Object.keys(t).forEach((r=>{e[r]=t[r]}))})(h,e)}function u(t,a){const l=document.createElement("style");l.innerHTML="body { margin:0; } \n  @media (prefers-color-scheme: dark) {\n    body {\n      background-color: #111111;\n      color: #e1e1e1;\n    }\n  }",document.head.appendChild(l);const u=t.config._panel_custom;let v=Promise.resolve();o||(v=v.then((()=>r("/static/polyfills/webcomponents-bundle.js")))),v.then((()=>c(u))).then((()=>d||Promise.resolve())).then((()=>{h=(e=>{const t="html_url"in e?`ha-panel-${e.name}`:e.name;return document.createElement(t)})(u);h.addEventListener("hass-toggle-menu",(t=>{window.parent.customPanel&&(0,e.B)(window.parent.customPanel,t.type,t.detail)})),window.addEventListener("location-changed",(e=>{window.parent.customPanel&&window.parent.customPanel.navigate(window.location.pathname,e.detail)})),p({panel:t,...a}),document.body.appendChild(h)}),(e=>{let r;console.error(e,t),"hassio"===t.url_path?(Promise.all([i.e(145),i.e(149),i.e(9849),i.e(1479),i.e(6134),i.e(2678)]).then(i.bind(i,82678)),r=document.createElement("supervisor-error-screen")):(Promise.all([i.e(149),i.e(9849),i.e(6134),i.e(2024)]).then(i.bind(i,48811)),r=document.createElement("hass-error-screen"),r.error=`Unable to load the panel source: ${e}.`);const o=document.createElement("style");o.innerHTML=s.e$.cssText,document.body.appendChild(o),r.hass=a.hass,document.body.appendChild(r)})),document.body.addEventListener("click",(t=>{const r=(e=>{if(e.defaultPrevented||0!==e.button||e.metaKey||e.ctrlKey||e.shiftKey)return;const t=e.composedPath().filter((e=>"A"===e.tagName))[0];if(!t||t.target||t.hasAttribute("download")||"external"===t.getAttribute("rel"))return;let r=t.href;if(!r||-1!==r.indexOf("mailto:"))return;const o=window.location,i=o.origin||o.protocol+"//"+o.host;return 0===r.indexOf(i)&&(r=r.substr(i.length),"#"!==r)?(e.preventDefault(),r):void 0})(t);r&&((t,r)=>{const o=(null==r?void 0:r.replace)||!1;var i;o?n.history.replaceState(null!==(i=n.history.state)&&void 0!==i&&i.root?{root:!0}:null,"",t):n.history.pushState(null,"",t),(0,e.B)(n,"location-changed",{replace:o})})(r)}))}window.loadES5Adapter=()=>(d||(d=r("/static/polyfills/custom-elements-es5-adapter.js").catch()),d),document.addEventListener("DOMContentLoaded",(()=>window.parent.customPanel.registerIframe(u,p)),{once:!0})})()})();
//# sourceMappingURL=custom-panel.1d1b72c7.js.map