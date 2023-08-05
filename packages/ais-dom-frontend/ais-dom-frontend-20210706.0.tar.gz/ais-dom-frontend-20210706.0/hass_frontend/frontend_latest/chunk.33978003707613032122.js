(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[70151],{43274:(t,e,r)=>{"use strict";r.d(e,{Sb:()=>i,BF:()=>n,Op:()=>o});const i=function(){try{(new Date).toLocaleDateString("i")}catch(t){return"RangeError"===t.name}return!1}(),n=function(){try{(new Date).toLocaleTimeString("i")}catch(t){return"RangeError"===t.name}return!1}(),o=function(){try{(new Date).toLocaleString("i")}catch(t){return"RangeError"===t.name}return!1}()},44583:(t,e,r)=>{"use strict";r.d(e,{o:()=>c,E:()=>d});var i=r(68928),n=r(14516),o=r(43274),a=r(65810);const s=(0,n.Z)((t=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",hour12:(0,a.y)(t)}))),c=o.Op?(t,e)=>s(e).format(t):(t,e)=>(0,i.WU)(t,((0,a.y)(e)," A")),l=(0,n.Z)((t=>new Intl.DateTimeFormat(t.language,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit",second:"2-digit",hour12:(0,a.y)(t)}))),d=o.Op?(t,e)=>l(e).format(t):(t,e)=>(0,i.WU)(t,((0,a.y)(e)," A"))},65810:(t,e,r)=>{"use strict";r.d(e,{y:()=>n});var i=r(66477);const n=t=>{if(t.time_format===i.zt.language||t.time_format===i.zt.system){const e=t.time_format===i.zt.language?t.language:void 0,r=(new Date).toLocaleString(e);return r.includes("AM")||r.includes("PM")}return t.time_format===i.zt.am_pm}},25516:(t,e,r)=>{"use strict";r.d(e,{i:()=>i});const i=t=>e=>({kind:"method",placement:"prototype",key:e.key,descriptor:{set(t){this[`__${String(e.key)}`]=t},get(){return this[`__${String(e.key)}`]},enumerable:!0,configurable:!0},finisher(r){const i=r.prototype.connectedCallback;r.prototype.connectedCallback=function(){if(i.call(this),this[e.key]){const r=this.renderRoot.querySelector(t);if(!r)return;r.scrollTop=this[e.key]}}}})},96151:(t,e,r)=>{"use strict";r.d(e,{T:()=>i,y:()=>n});const i=t=>{requestAnimationFrame((()=>setTimeout(t,0)))},n=()=>new Promise((t=>{i(t)}))},93748:(t,e,r)=>{"use strict";r.d(e,{Es:()=>n,SC:()=>o,cV:()=>s,Ip:()=>c,Pl:()=>l});var i=r(83849);const n=(t,e)=>{t.callService("automation","trigger",{entity_id:e,skip_condition:!0})},o=(t,e)=>t.callApi("DELETE",`config/automation/config/${e}`);let a;const s=(t,e)=>t.callApi("GET",`config/automation/config/${e}`),c=t=>{a=t,(0,i.c)("/config/automation/edit/new")},l=()=>{const t=a;return a=void 0,t}},56007:(t,e,r)=>{"use strict";r.d(e,{nZ:()=>i,lz:()=>n,V_:()=>o});const i="unavailable",n="unknown",o=[i,n]},83114:(t,e,r)=>{"use strict";r.r(e);r(22098),r(48932),r(25230);var i=r(68546),n=(r(54444),r(50424)),o=r(55358),a=(r(42173),r(47181)),s=r(83849),c=(r(47150),r(36125),r(52039),r(67556),r(93748)),l=r(11654),d=r(22311),u=r(44583),h=r(14516);r(67065);function p(){p=function(){return t};var t={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(t,e){["method","field"].forEach((function(r){e.forEach((function(e){e.kind===r&&"own"===e.placement&&this.defineClassElement(t,e)}),this)}),this)},initializeClassElements:function(t,e){var r=t.prototype;["method","field"].forEach((function(i){e.forEach((function(e){var n=e.placement;if(e.kind===i&&("static"===n||"prototype"===n)){var o="static"===n?t:r;this.defineClassElement(o,e)}}),this)}),this)},defineClassElement:function(t,e){var r=e.descriptor;if("field"===e.kind){var i=e.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(t)}}Object.defineProperty(t,e.key,r)},decorateClass:function(t,e){var r=[],i=[],n={static:[],prototype:[],own:[]};if(t.forEach((function(t){this.addElementPlacement(t,n)}),this),t.forEach((function(t){if(!y(t))return r.push(t);var e=this.decorateElement(t,n);r.push(e.element),r.push.apply(r,e.extras),i.push.apply(i,e.finishers)}),this),!e)return{elements:r,finishers:i};var o=this.decorateConstructor(r,e);return i.push.apply(i,o.finishers),o.finishers=i,o},addElementPlacement:function(t,e,r){var i=e[t.placement];if(!r&&-1!==i.indexOf(t.key))throw new TypeError("Duplicated element ("+t.key+")");i.push(t.key)},decorateElement:function(t,e){for(var r=[],i=[],n=t.decorators,o=n.length-1;o>=0;o--){var a=e[t.placement];a.splice(a.indexOf(t.key),1);var s=this.fromElementDescriptor(t),c=this.toElementFinisherExtras((0,n[o])(s)||s);t=c.element,this.addElementPlacement(t,e),c.finisher&&i.push(c.finisher);var l=c.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],e);r.push.apply(r,l)}}return{element:t,finishers:i,extras:r}},decorateConstructor:function(t,e){for(var r=[],i=e.length-1;i>=0;i--){var n=this.fromClassDescriptor(t),o=this.toClassDescriptor((0,e[i])(n)||n);if(void 0!==o.finisher&&r.push(o.finisher),void 0!==o.elements){t=o.elements;for(var a=0;a<t.length-1;a++)for(var s=a+1;s<t.length;s++)if(t[a].key===t[s].key&&t[a].placement===t[s].placement)throw new TypeError("Duplicated element ("+t[a].key+")")}}return{elements:t,finishers:r}},fromElementDescriptor:function(t){var e={kind:t.kind,key:t.key,placement:t.placement,descriptor:t.descriptor};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===t.kind&&(e.initializer=t.initializer),e},toElementDescriptors:function(t){var e;if(void 0!==t)return(e=t,function(t){if(Array.isArray(t))return t}(e)||function(t){if("undefined"!=typeof Symbol&&null!=t[Symbol.iterator]||null!=t["@@iterator"])return Array.from(t)}(e)||function(t,e){if(t){if("string"==typeof t)return k(t,e);var r=Object.prototype.toString.call(t).slice(8,-1);return"Object"===r&&t.constructor&&(r=t.constructor.name),"Map"===r||"Set"===r?Array.from(t):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?k(t,e):void 0}}(e)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(t){var e=this.toElementDescriptor(t);return this.disallowProperty(t,"finisher","An element descriptor"),this.disallowProperty(t,"extras","An element descriptor"),e}),this)},toElementDescriptor:function(t){var e=String(t.kind);if("method"!==e&&"field"!==e)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+e+'"');var r=b(t.key),i=String(t.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var n=t.descriptor;this.disallowProperty(t,"elements","An element descriptor");var o={kind:e,key:r,placement:i,descriptor:Object.assign({},n)};return"field"!==e?this.disallowProperty(t,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=t.initializer),o},toElementFinisherExtras:function(t){return{element:this.toElementDescriptor(t),finisher:v(t,"finisher"),extras:this.toElementDescriptors(t.extras)}},fromClassDescriptor:function(t){var e={kind:"class",elements:t.map(this.fromElementDescriptor,this)};return Object.defineProperty(e,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),e},toClassDescriptor:function(t){var e=String(t.kind);if("class"!==e)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+e+'"');this.disallowProperty(t,"key","A class descriptor"),this.disallowProperty(t,"placement","A class descriptor"),this.disallowProperty(t,"descriptor","A class descriptor"),this.disallowProperty(t,"initializer","A class descriptor"),this.disallowProperty(t,"extras","A class descriptor");var r=v(t,"finisher");return{elements:this.toElementDescriptors(t.elements),finisher:r}},runClassFinishers:function(t,e){for(var r=0;r<e.length;r++){var i=(0,e[r])(t);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");t=i}}return t},disallowProperty:function(t,e,r){if(void 0!==t[e])throw new TypeError(r+" can't have a ."+e+" property.")}};return t}function f(t){var e,r=b(t.key);"method"===t.kind?e={value:t.value,writable:!0,configurable:!0,enumerable:!1}:"get"===t.kind?e={get:t.value,configurable:!0,enumerable:!1}:"set"===t.kind?e={set:t.value,configurable:!0,enumerable:!1}:"field"===t.kind&&(e={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===t.kind?"field":"method",key:r,placement:t.static?"static":"field"===t.kind?"own":"prototype",descriptor:e};return t.decorators&&(i.decorators=t.decorators),"field"===t.kind&&(i.initializer=t.value),i}function m(t,e){void 0!==t.descriptor.get?e.descriptor.get=t.descriptor.get:e.descriptor.set=t.descriptor.set}function y(t){return t.decorators&&t.decorators.length}function g(t){return void 0!==t&&!(void 0===t.value&&void 0===t.writable)}function v(t,e){var r=t[e];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+e+"' to be a function");return r}function b(t){var e=function(t,e){if("object"!=typeof t||null===t)return t;var r=t[Symbol.toPrimitive];if(void 0!==r){var i=r.call(t,e||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===e?String:Number)(t)}(t,"string");return"symbol"==typeof e?e:String(e)}function k(t,e){(null==e||e>t.length)&&(e=t.length);for(var r=0,i=new Array(e);r<e;r++)i[r]=t[r];return i}function w(t,e,r){return(w="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(t,e,r){var i=function(t,e){for(;!Object.prototype.hasOwnProperty.call(t,e)&&null!==(t=E(t)););return t}(t,e);if(i){var n=Object.getOwnPropertyDescriptor(i,e);return n.get?n.get.call(r):n.value}})(t,e,r||t)}function E(t){return(E=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)})(t)}!function(t,e,r,i){var n=p();if(i)for(var o=0;o<i.length;o++)n=i[o](n);var a=e((function(t){n.initializeInstanceElements(t,s.elements)}),r),s=n.decorateClass(function(t){for(var e=[],r=function(t){return"method"===t.kind&&t.key===o.key&&t.placement===o.placement},i=0;i<t.length;i++){var n,o=t[i];if("method"===o.kind&&(n=e.find(r)))if(g(o.descriptor)||g(n.descriptor)){if(y(o)||y(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(y(o)){if(y(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}m(o,n)}else e.push(o)}return e}(a.d.map(f)),t);n.initializeClassElements(a.F,s.elements),n.runClassFinishers(a.F,s.finishers)}([(0,o.Mo)("ha-panel-aisttsauto")],(function(t,e){class r extends e{constructor(...e){super(...e),t(this)}}return{F:r,d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",key:"_columns",value(){return(0,h.Z)(((t,e)=>{const r={toggle:{title:n.dy`&nbsp;&nbsp;&nbsp;&nbsp;<ha-svg-icon
              path=${i.L2n}
            ></ha-svg-icon>`,type:"icon",template:(t,e)=>n.dy`
              <ha-checkbox
                .key=${e.id}
                .hass=${this.hass}
                @change=${this._handleRowCheckboxClick}
                .checked=${"on"===e.entity.state}
              >
              </ha-checkbox>
            `},name:{title:"Nazwa",sortable:!0,filterable:!0,direction:"asc",grows:!0}};return t||(r.last_triggered={sortable:!0,width:"20%",title:this.hass.localize("ui.card.automation.last_triggered"),template:t=>n.dy`
            ${t?(0,u.o)(new Date(t),this.hass.locale):this.hass.localize("ui.components.relative_time.never")}
          `},r.trigger={title:n.dy`
            <mwc-button style="visibility: hidden">
              ${this.hass.localize("ui.card.automation.trigger")}
            </mwc-button>
          `,width:"20%",template:(t,e)=>n.dy`
            <mwc-button
              .automation=${e.entity}
              @click=${t=>this._runActions(t)}
            >
              URUCHOM
            </mwc-button>
          `}),this.hass.user.is_admin&&(r.info={title:"",type:"icon-button",template:(t,e)=>n.dy`
            <mwc-icon-button
              .automation=${e.entity}
              @click=${this._showInfo}
              label="Info"
            >
              <ha-svg-icon .path=${i.EaN}></ha-svg-icon>
            </mwc-icon-button>
          `},r.trace={title:"",type:"icon-button",template:(t,e)=>n.dy`
            <a
              href="/config/automation/trace/${e.entity.attributes.id}"
            >
              <mwc-icon-button label="Ślad">
                <ha-svg-icon .path=${i.BBX}></ha-svg-icon>
              </mwc-icon-button>
            </a>
          `},r.edit={title:"",type:"icon-button",template:(t,e)=>n.dy`
            <a
              href="/config/automation/edit/${e.entity.attributes.id}"
            >
              <mwc-icon-button label="Edit">
                <ha-svg-icon path=${i.r9}></ha-svg-icon>
              </mwc-icon-button>
            </a>
          `}),r}))}},{kind:"method",key:"firstUpdated",value:function(t){w(E(r.prototype),"firstUpdated",this).call(this,t)}},{kind:"method",key:"_get_automations",value:function(t){const e=[];return Object.values(this.hass.states).forEach((t=>{"automation"!==(0,d.N)(t)||t.entity_id.startsWith("automation.ais_")||e.push({id:t.entity_id,name:t.attributes.friendly_name,last_triggered:t.attributes.last_triggered,entity:t})})),e}},{kind:"method",key:"render",value:function(){return n.dy`
      <ha-app-layout>
        <app-header slot="header" fixed>
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <div main-title>TTS Automatyczny</div>
            ${this.hass.user.is_admin?n.dy`<ha-icon-button
                  label="Dodaj"
                  icon="hass:plus"
                  @click=${this._createNew}
                ></ha-icon-button>`:n.dy``}
          </app-toolbar>
        </app-header>
        <ha-card class="content">
          <ha-data-table
            .columns=${this._columns(this.narrow,this.hass.locale)}
            .data=${this._get_automations(this.hass.states)}
            auto-height
            searchLabel="Szukaj"
            noDataText="Brak danych"
          ></ha-data-table>
        </ha-card>
      </ha-app-layout>
    `}},{kind:"method",key:"_showInfo",value:function(t){t.stopPropagation();const e=t.currentTarget.automation.entity_id;(0,a.B)(this,"hass-more-info",{entityId:e})}},{kind:"method",key:"_runActions",value:function(t){const e=t.currentTarget.automation.entity_id;(0,c.Es)(this.hass,e)}},{kind:"method",key:"_createNew",value:function(){(0,s.c)("/config/automation/edit/new")}},{kind:"method",key:"_handleRowCheckboxClick",value:function(t){const e=t.currentTarget.key,r=t.currentTarget.hass;let i="off";t.currentTarget.checked&&(i="on"),r.callService("ais_tts","change_auto_mode",{entity_id:e,change_to:i})}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,n.iv`
        ha-card.content {
          padding: 16px;
        }

        .has-header {
          padding-top: 0;
        }

        .checked span {
          color: var(--primary-color);
        }
        .content {
          padding-bottom: 32px;
          max-width: 94%;
          margin: 0 auto;
        }
      `]}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.33978003707613032122.js.map