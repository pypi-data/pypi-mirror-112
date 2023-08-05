(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[33137],{85415:(e,t,r)=>{"use strict";r.d(t,{q:()=>i,w:()=>o});const i=(e,t)=>e<t?-1:e>t?1:0,o=(e,t)=>i(e.toLowerCase(),t.toLowerCase())},73728:(e,t,r)=>{"use strict";r.d(t,{pV:()=>s,P3:()=>a,Ky:()=>c,D4:()=>d,XO:()=>p,zO:()=>f,oi:()=>h,d4:()=>u,D7:()=>m,ZJ:()=>v,V3:()=>y,WW:()=>g});var i=r(95282),o=r(38346),n=r(5986);const s=["unignore","dhcp","homekit","ssdp","zeroconf","discovery","mqtt","hassio"],a=["reauth"],l={"HA-Frontend-Base":`${location.protocol}//${location.host}`},c=(e,t)=>{var r;return e.callApi("POST","config/config_entries/flow",{handler:t,show_advanced_options:Boolean(null===(r=e.userData)||void 0===r?void 0:r.showAdvanced)},l)},d=(e,t)=>e.callApi("GET",`config/config_entries/flow/${t}`,void 0,l),p=(e,t,r)=>e.callApi("POST",`config/config_entries/flow/${t}`,r,l),f=(e,t,r)=>e.callWS({type:"config_entries/ignore_flow",flow_id:t,title:r}),h=(e,t)=>e.callApi("DELETE",`config/config_entries/flow/${t}`),u=e=>e.callApi("GET","config/config_entries/flow_handlers"),m=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),w=(e,t)=>e.subscribeEvents((0,o.D)((()=>m(e).then((e=>t.setState(e,!0)))),500,!0),"config_entry_discovered"),v=e=>(0,i._)(e,"_configFlowProgress",m,w),y=(e,t)=>v(e.connection).subscribe(t),g=(e,t)=>{const r=t.context.title_placeholders||{},i=Object.keys(r);if(0===i.length)return(0,n.Lh)(e,t.handler);const o=[];return i.forEach((e=>{o.push(e),o.push(r[e])})),e(`component.${t.handler}.config.flow_title`,...o)}},2852:(e,t,r)=>{"use strict";r.d(t,{t:()=>l});var i=r(50424),o=r(85415),n=r(73728),s=r(5986),a=r(52871);const l=(e,t)=>(0,a.w)(e,t,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[t]=await Promise.all([(0,n.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return t.sort(((t,r)=>(0,o.w)((0,s.Lh)(e.localize,t),(0,s.Lh)(e.localize,r))))},createFlow:async(e,t)=>{const[r]=await Promise.all([(0,n.Ky)(e,t),e.loadBackendTranslation("config",t)]);return r},fetchFlow:async(e,t)=>{const r=await(0,n.D4)(e,t);return await e.loadBackendTranslation("config",r.handler),r},handleFlowStep:n.XO,deleteFlow:n.oi,renderAbortDescription(e,t){const r=e.localize(`component.${t.handler}.config.abort.${t.reason}`,t.description_placeholders);return r?i.dy`
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
          `:""}})},52871:(e,t,r)=>{"use strict";r.d(t,{w:()=>n});var i=r(47181);const o=()=>Promise.all([r.e(75009),r.e(78161),r.e(42955),r.e(68200),r.e(30879),r.e(13967),r.e(1041),r.e(91657),r.e(30486),r.e(81480),r.e(67024),r.e(82374),r.e(16509),r.e(68331),r.e(68101),r.e(4940),r.e(40091),r.e(33258)]).then(r.bind(r,27234)),n=(e,t,r)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:o,dialogParams:{...t,flowConfig:r}})}},33137:(e,t,r)=>{"use strict";r.r(t);r(53268),r(12730),r(60010),r(38353),r(63081);var i=r(2852),o=r(47181),n=r(50424),s=r(55358),a=r(11654);function l(){l=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(r){t.forEach((function(t){t.kind===r&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var r=e.prototype;["method","field"].forEach((function(i){t.forEach((function(t){var o=t.placement;if(t.kind===i&&("static"===o||"prototype"===o)){var n="static"===o?e:r;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var r=t.descriptor;if("field"===t.kind){var i=t.initializer;r={enumerable:r.enumerable,writable:r.writable,configurable:r.configurable,value:void 0===i?void 0:i.call(e)}}Object.defineProperty(e,t.key,r)},decorateClass:function(e,t){var r=[],i=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!p(e))return r.push(e);var t=this.decorateElement(e,o);r.push(t.element),r.push.apply(r,t.extras),i.push.apply(i,t.finishers)}),this),!t)return{elements:r,finishers:i};var n=this.decorateConstructor(r,t);return i.push.apply(i,n.finishers),n.finishers=i,n},addElementPlacement:function(e,t,r){var i=t[e.placement];if(!r&&-1!==i.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");i.push(e.key)},decorateElement:function(e,t){for(var r=[],i=[],o=e.decorators,n=o.length-1;n>=0;n--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,o[n])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&i.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);r.push.apply(r,c)}}return{element:e,finishers:i,extras:r}},decorateConstructor:function(e,t){for(var r=[],i=t.length-1;i>=0;i--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[i])(o)||o);if(void 0!==n.finisher&&r.push(n.finisher),void 0!==n.elements){e=n.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:r}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return m(e,t);var r=Object.prototype.toString.call(e).slice(8,-1);return"Object"===r&&e.constructor&&(r=e.constructor.name),"Map"===r||"Set"===r?Array.from(e):"Arguments"===r||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r)?m(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var r=u(e.key),i=String(e.placement);if("static"!==i&&"prototype"!==i&&"own"!==i)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+i+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:r,placement:i,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var r=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:r}},runClassFinishers:function(e,t){for(var r=0;r<t.length;r++){var i=(0,t[r])(e);if(void 0!==i){if("function"!=typeof i)throw new TypeError("Finishers must return a constructor.");e=i}}return e},disallowProperty:function(e,t,r){if(void 0!==e[t])throw new TypeError(r+" can't have a ."+t+" property.")}};return e}function c(e){var t,r=u(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var i={kind:"field"===e.kind?"field":"method",key:r,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(i.decorators=e.decorators),"field"===e.kind&&(i.initializer=e.value),i}function d(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function p(e){return e.decorators&&e.decorators.length}function f(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var r=e[t];if(void 0!==r&&"function"!=typeof r)throw new TypeError("Expected '"+t+"' to be a function");return r}function u(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var r=e[Symbol.toPrimitive];if(void 0!==r){var i=r.call(e,t||"default");if("object"!=typeof i)return i;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function m(e,t){(null==t||t>e.length)&&(t=e.length);for(var r=0,i=new Array(t);r<t;r++)i[r]=e[r];return i}!function(e,t,r,i){var o=l();if(i)for(var n=0;n<i.length;n++)o=i[n](o);var s=t((function(e){o.initializeInstanceElements(e,a.elements)}),r),a=o.decorateClass(function(e){for(var t=[],r=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},i=0;i<e.length;i++){var o,n=e[i];if("method"===n.kind&&(o=t.find(r)))if(f(n.descriptor)||f(o.descriptor)){if(p(n)||p(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(p(n)){if(p(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}d(n,o)}else t.push(n)}return t}(s.d.map(c)),e);o.initializeClassElements(s.F,a.elements),o.runClassFinishers(s.F,a.finishers)}([(0,s.Mo)("ha-config-ais-dom-config-wifi")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,s.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"isWide",value:()=>!0},{kind:"field",decorators:[(0,s.Cb)({type:Boolean})],key:"narrow",value:()=>!1},{kind:"method",key:"firstUpdated",value:async function(){}},{kind:"method",key:"render",value:function(){return this.hass?n.dy`
      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div .narrow=${this.narrow}>
          <ha-config-section .isWide=${this.isWide}>
            <span slot="header">Połączenie WiFi</span>
            <span slot="introduction"
              >Możesz sprawdzić lub skonfigurować parametry połączenia
              WiFi</span
            >
            <ha-card header="Parametry sieci">
              <div class="card-content" style="display: flex;">
                <div style="text-align: center;">
                  <div class="aisInfoRow">Lokalna nazwa hosta</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.local_host_name"].state}</mwc-button
                    >
                    <ha-icon-button
                      class="user-button"
                      icon="hass:cog"
                      @click=${this.createFlowHostName}
                    ></ha-icon-button>
                  </div>
                </div>
                <div style="text-align: center;" @click=${this.showLocalIpInfo}>
                  <div class="aisInfoRow">Lokalny adres IP</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.internal_ip_address"].state}</mwc-button
                    >
                  </div>
                </div>
                <div
                  @click=${this.showWiFiSpeedInfo}
                  style="text-align: center;"
                >
                  <div class="aisInfoRow">Prędkość połączenia WiFi</div>
                  <div class="aisInfoRow">
                    <mwc-button
                      >${this.hass.states["sensor.ais_wifi_service_current_network_info"].state}</mwc-button
                    >
                  </div>
                </div>
              </div>
              <div class="card-actions">
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:wifi"
                    @click=${this.showWiFiGroup}
                  ></ha-icon-button
                  ><mwc-button @click=${this.createFlowWifi}
                    >Konfigurator połączenia z siecą WiFi</mwc-button
                  >
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `:n.dy``}},{kind:"get",static:!0,key:"styles",value:function(){return[a.Qx,n.iv`
        .content {
          padding-bottom: 32px;
        }
        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        div.aisInfoRow {
          display: inline-block;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        ha-icon-button {
          vertical-align: middle;
        }
      `]}},{kind:"method",key:"showWiFiGroup",value:function(){(0,o.B)(this,"hass-more-info",{entityId:"group.internet_status"})}},{kind:"method",key:"showWiFiSpeedInfo",value:function(){(0,o.B)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}},{kind:"method",key:"showLocalIpInfo",value:function(){(0,o.B)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}},{kind:"method",key:"_continueFlow",value:function(e){(0,i.t)(this,{continueFlowId:e,dialogClosedCallback:()=>{console.log("OK")}})}},{kind:"method",key:"createFlowHostName",value:function(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then((e=>{this._continueFlow(e.flow_id)}))}},{kind:"method",key:"createFlowWifi",value:function(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then((e=>{console.log(e),this._continueFlow(e.flow_id)}))}}]}}),n.oi)}}]);
//# sourceMappingURL=chunk.0a190f51ca17b3ac1b80.js.map