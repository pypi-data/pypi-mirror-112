/*! For license information please see chunk.2fc4361491dbd413a54f.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[14222],{96151:(e,t,r)=>{"use strict";r.d(t,{T:()=>i,y:()=>n});const i=e=>{requestAnimationFrame((()=>setTimeout(e,0)))},n=()=>new Promise((e=>{i(e)}))},2852:(e,t,r)=>{"use strict";r.d(t,{t:()=>l});var i=r(50424),n=r(85415),o=r(73728),a=r(5986),s=r(52871);const l=(e,t)=>(0,s.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,o.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,r)=>(0,n.w)((0,a.Lh)(e.localize,t),(0,a.Lh)(e.localize,r))))},createFlow:async(e,t)=>{const[r]=await Promise.all([(0,o.Ky)(e,t),e.loadBackendTranslation("config",t)]);return r},fetchFlow:async(e,t)=>{const r=await(0,o.D4)(e,t);return await e.loadBackendTranslation("config",r.handler),r},handleFlowStep:o.XO,deleteFlow:o.oi,renderAbortDescription(e,t){const r=e.localize(`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormStepDescription(e,t){const r=e.localize(`component.${t.handler}.config.step.${t.step_id}.description`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,t,r)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.data.${r.name}`),renderShowFormStepFieldError:(e,t,r)=>e.localize(`component.${t.handler}.config.error.${r}`,t.description_placeholders),renderExternalStepHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,t){const r=e.localize(`component.${t.handler}.config.${t.step_id}.description`,t.description_placeholders);return i.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${r?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,t){const r=e.localize(`component.${t.handler}.config.create_entry.${t.description||"default"}`,t.description_placeholders);return i.dy`
        ${r?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${r}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",t.title)}
        </p>
      `},renderShowFormProgressHeader:(e,t)=>e.localize(`component.${t.handler}.config.step.${t.step_id}.title`)||e.localize(`component.${t.handler}.title`),renderShowFormProgressDescription(e,t){const r=e.localize(`component.${t.handler}.config.progress.${t.progress_action}`,t.description_placeholders);return r?i.dy`
            <ha-markdown allowsvg breaks .content=${r}></ha-markdown>
          `:""}})},52871:(e,t,r)=>{"use strict";r.d(t,{w:()=>o});var i=r(47181);const n=()=>Promise.all([r.e(75009),r.e(78161),r.e(42955),r.e(68200),r.e(30879),r.e(13967),r.e(1041),r.e(91657),r.e(30486),r.e(81480),r.e(67024),r.e(82374),r.e(16509),r.e(68331),r.e(68101),r.e(4940),r.e(40091),r.e(33258)]).then(r.bind(r,27234)),o=(e,t,r)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:{...t,flowConfig:r}})}},51444:(e,t,r)=>{"use strict";r.d(t,{_:()=>o});var i=r(47181);const n=()=>Promise.all([r.e(75009),r.e(81199),r.e(72420)]).then(r.bind(r,72420)),o=e=>{(0,i.B)(e,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:n,dialogParams:{}})}},27849:(e,t,r)=>{"use strict";r(39841);var i=r(50856);r(28426);class n extends(customElements.get("app-header-layout")){static get template(){return i.d`
      <style>
        :host {
          display: block;
          /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
          position: relative;
          z-index: 0;
        }

        #wrapper ::slotted([slot="header"]) {
          @apply --layout-fixed-top;
          z-index: 1;
        }

        #wrapper.initializing ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) {
          height: 100%;
        }

        :host([has-scrolling-region]) #wrapper ::slotted([slot="header"]) {
          position: absolute;
        }

        :host([has-scrolling-region])
          #wrapper.initializing
          ::slotted([slot="header"]) {
          position: relative;
        }

        :host([has-scrolling-region]) #wrapper #contentContainer {
          @apply --layout-fit;
          overflow-y: auto;
          -webkit-overflow-scrolling: touch;
        }

        :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
          position: relative;
        }

        #contentContainer {
          /* Create a stacking context here so that all children appear below the header. */
          position: relative;
          z-index: 0;
          /* Using 'transform' will cause 'position: fixed' elements to behave like
           'position: absolute' relative to this element. */
          transform: translate(0);
          margin-left: env(safe-area-inset-left);
          margin-right: env(safe-area-inset-right);
        }

        @media print {
          :host([has-scrolling-region]) #wrapper #contentContainer {
            overflow-y: visible;
          }
        }
      </style>

      <div id="wrapper" class="initializing">
        <slot id="headerSlot" name="header"></slot>

        <div id="contentContainer"><slot></slot></div>
        <slot id="fab" name="fab"></slot>
      </div>
    `}}customElements.define("ha-app-layout",n)},51153:(e,t,r)=>{"use strict";r.d(t,{l$:()=>a,Z6:()=>s,Do:()=>l});r(49072),r(72225),r(26654),r(10175),r(80251),r(99471),r(14888),r(69377),r(95035),r(38026),r(89173),r(41043),r(57464),r(24617),r(26136),r(82778),r(28738),r(55227),r(43868);var i=r(7778);const n=new Set(["ais-easy-picker","ais-button","ais-files-list","entity","entities","button","entity-button","glance","history-graph","horizontal-stack","light","sensor","thermostat","vertical-stack","weather-forecast","ais-zigbee2mqtt","ais-mini-media-player","ais-expansion-panel"]),o={"alarm-panel":()=>r.e(77639).then(r.bind(r,77639)),error:()=>Promise.all([r.e(98595),r.e(55796)]).then(r.bind(r,55796)),"empty-state":()=>r.e(67284).then(r.bind(r,67284)),grid:()=>r.e(6169).then(r.bind(r,6169)),starting:()=>r.e(47873).then(r.bind(r,47873)),"entity-filter":()=>r.e(33688).then(r.bind(r,33688)),humidifier:()=>r.e(68558).then(r.bind(r,68558)),"media-control":()=>Promise.all([r.e(67794),r.e(13525)]).then(r.bind(r,13525)),"picture-elements":()=>Promise.all([r.e(54909),r.e(319),r.e(6315),r.e(97282),r.e(99810),r.e(61267)]).then(r.bind(r,83358)),"picture-entity":()=>Promise.all([r.e(319),r.e(97282),r.e(44649)]).then(r.bind(r,41500)),"picture-glance":()=>Promise.all([r.e(319),r.e(97282),r.e(81721)]).then(r.bind(r,66621)),"plant-status":()=>r.e(48723).then(r.bind(r,48723)),"safe-mode":()=>r.e(24503).then(r.bind(r,24503)),"shopping-list":()=>r.e(43376).then(r.bind(r,43376)),conditional:()=>r.e(68857).then(r.bind(r,68857)),gauge:()=>r.e(25223).then(r.bind(r,25223)),iframe:()=>r.e(95018).then(r.bind(r,95018)),map:()=>Promise.all([r.e(29389),r.e(60076)]).then(r.bind(r,60076)),markdown:()=>Promise.all([r.e(4940),r.e(86474)]).then(r.bind(r,51282)),picture:()=>r.e(45338).then(r.bind(r,45338)),"ais-list":()=>r.e(1401).then(r.t.bind(r,1401,23)),"ais-auto-entities":()=>r.e(82657).then(r.t.bind(r,82657,23)),"ais-monster":()=>r.e(47680).then(r.t.bind(r,47680,23)),"ais-fold-entity-row":()=>r.e(9795).then(r.t.bind(r,9795,23)),"ais-now-playing-poster":()=>r.e(86327).then(r.bind(r,86327)),"ais-light":()=>r.e(63238).then(r.bind(r,63238)),calendar:()=>Promise.resolve().then(r.bind(r,80251)),logbook:()=>Promise.all([r.e(83511),r.e(81855),r.e(94302)]).then(r.bind(r,8436))},a=e=>(0,i.Xm)("card",e,n,o,void 0,void 0),s=e=>(0,i.Tw)("card",e,n,o,void 0,void 0),l=e=>(0,i.ED)(e,"card",n,o)},89026:(e,t,r)=>{"use strict";r.d(t,{t:()=>o,Q:()=>a});var i=r(7778);const n={picture:()=>r.e(69130).then(r.bind(r,69130)),buttons:()=>r.e(32587).then(r.bind(r,32587)),graph:()=>r.e(25773).then(r.bind(r,25773))},o=e=>(0,i.Tw)("header-footer",e,void 0,n,void 0,void 0),a=e=>(0,i.ED)(e,"header-footer",void 0,n)},44295:(e,t,r)=>{"use strict";r.r(t);var i=r(68546),n=(r(53268),r(12730),r(50424)),o=r(55358),a=r(14516),s=r(7323),l=(r(48932),r(51444)),c=(r(27849),r(11654)),d=r(51153);function p(){p=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var n=t.placement;if(t.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?e:r;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!u(e))return r.push(e);var t=this.decorateElement(e,n);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var o=this.decorateConstructor(r,t);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],n=e.decorators,o=n.length-1;o>=0;o--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(s)||s);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){e=o.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=y(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function h(e){var t,r=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function f(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}function w(e,t,r){return(w="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,r){var i=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=b(e)););return e}(e,t);if(i){var n=Object.getOwnPropertyDescriptor(i,t);return n.get?n.get.call(r):n.value}})(e,t,r||e)}function b(e){return(b=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}!function(e,t,r,i){var n=p();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=t((function(e){n.initializeInstanceElements(e,s.elements)}),r),s=n.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},i=0;i<e.length;i++){var n,o=e[i];if("method"===o.kind&&(n=t.find(r)))if(m(o.descriptor)||m(n.descriptor)){if(u(o)||u(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(u(o)){if(u(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}f(o,n)}else t.push(o)}return t}(a.d.map(h)),e);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,o.Mo)("ha-panel-shopping-list")],(function(e,t){class r extends t{constructor(...t){super(...t),e(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,o.SB)()],key:"_card",value:void 0},{kind:"field",key:"_conversation",value(){return(0,a.Z)((e=>(0,s.p)(this.hass,"conversation")))}},{kind:"method",key:"firstUpdated",value:function(e){w(b(r.prototype),"firstUpdated",this).call(this,e),this._card=(0,d.Z6)({type:"shopping-list"}),this._card.hass=this.hass}},{kind:"method",key:"updated",value:function(e){w(b(r.prototype),"updated",this).call(this,e),e.has("hass")&&(this._card.hass=this.hass)}},{kind:"method",key:"render",value:function(){return n.dy`
      <ha-app-layout>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title>${this.hass.localize("panel.shopping_list")}</div>
            ${this._conversation(this.hass.config.components)?n.dy`
                  <mwc-icon-button
                    .label=${this.hass.localize("ui.panel.shopping_list.start_conversation")}
                    @click=${this._showVoiceCommandDialog}
                  >
                    <ha-svg-icon .path=${i.N3O}></ha-svg-icon>
                  </mwc-icon-button>
                `:""}
          </app-toolbar>
        </app-header>
        <div id="columns">
          <div class="column">${this._card}</div>
        </div>
      </ha-app-layout>
    `}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,l._)(this)}},{kind:"get",static:!0,key:"styles",value:function(){return[c.Qx,n.iv`
        :host {
          --mdc-theme-primary: var(--app-header-text-color);
          display: block;
          height: 100%;
        }
        :host([narrow]) app-toolbar mwc-button {
          width: 65px;
        }
        .heading {
          overflow: hidden;
          white-space: nowrap;
          margin-top: 4px;
        }
        #columns {
          display: flex;
          flex-direction: row;
          justify-content: center;
          margin-left: 4px;
          margin-right: 4px;
        }
        .column {
          flex: 1 0 0;
          max-width: 500px;
          min-width: 0;
        }
      `]}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.2fc4361491dbd413a54f.js.map