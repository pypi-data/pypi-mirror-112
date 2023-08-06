(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[53890],{53890:(e,t,i)=>{"use strict";i.r(t),i.d(t,{HaAutomationTrace:()=>T});var r=i(68546),o=i(50424),n=i(55358),a=i(76666),s=i(13690),c=i(7323),d=i(44583),l=(i(59679),i(55422)),h=i(97389),u=i(26765),p=i(11654),f=i(29311),v=(i(71955),i(13126),i(89497),i(78940),i(10678),i(19476));function m(){m=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var o=t.placement;if(t.kind===r&&("static"===o||"prototype"===o)){var n="static"===o?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!b(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],o=e.decorators,n=o.length-1;n>=0;n--){var a=t[e.placement];a.splice(a.indexOf(e.key),1);var s=this.fromElementDescriptor(e),c=this.toElementFinisherExtras((0,o[n])(s)||s);e=c.element,this.addElementPlacement(e,t),c.finisher&&r.push(c.finisher);var d=c.extras;if(d){for(var l=0;l<d.length;l++)this.addElementPlacement(d[l],t);i.push.apply(i,d)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var o=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(o)||o);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var a=0;a<e.length-1;a++)for(var s=a+1;s<e.length;s++)if(e[a].key===e[s].key&&e[a].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[a].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return $(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?$(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=w(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:g(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=g(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function y(e){var t,i=w(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function k(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function b(e){return e.decorators&&e.decorators.length}function _(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function g(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function w(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function $(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function E(e,t,i){return(E="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=I(e)););return e}(e,t);if(r){var o=Object.getOwnPropertyDescriptor(r,t);return o.get?o.get.call(i):o.value}})(e,t,i||e)}function I(e){return(I=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)})(e)}let T=function(e,t,i,r){var o=m();if(r)for(var n=0;n<r.length;n++)o=r[n](o);var a=t((function(e){o.initializeInstanceElements(e,s.elements)}),i),s=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var o,n=e[r];if("method"===n.kind&&(o=t.find(i)))if(_(n.descriptor)||_(o.descriptor)){if(b(n)||b(o))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");o.descriptor=n.descriptor}else{if(b(n)){if(b(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");o.decorators=n.decorators}k(n,o)}else t.push(n)}return t}(a.d.map(y)),e);return o.initializeClassElements(a.F,s.elements),o.runClassFinishers(a.F,s.finishers)}([(0,n.Mo)("ha-automation-trace")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.Cb)()],key:"automationId",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"automations",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,n.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,n.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_entityId",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_traces",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_runId",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_selected",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_trace",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_logbookEntries",value:void 0},{kind:"field",decorators:[(0,n.SB)()],key:"_view",value:()=>"details"},{kind:"method",key:"render",value:function(){var e;const t=this._entityId?this.hass.states[this._entityId]:void 0,i=this.shadowRoot.querySelector("hat-script-graph"),n=null==i?void 0:i.trackedNodes,c=null==i?void 0:i.renderedNodes,l=(null==t?void 0:t.attributes.friendly_name)||this._entityId;const h=o.dy`
      <mwc-icon-button label="Refresh" @click=${()=>this._loadTraces()}>
        <ha-svg-icon .path=${r.jcD}></ha-svg-icon>
      </mwc-icon-button>
      <mwc-icon-button
        .disabled=${!this._trace}
        label="Download Trace"
        @click=${this._downloadTrace}
      >
        <ha-svg-icon .path=${r.OGU}></ha-svg-icon>
      </mwc-icon-button>
    `;return o.dy`
      ${""}
      <hass-tabs-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .tabs=${f.configSections.automation}
      >
        ${this.narrow?o.dy`<span slot="header"> ${l} </span>
              <div slot="toolbar-icon">${h}</div>`:""}
        <div class="toolbar">
          ${this.narrow?"":o.dy`<div>
                ${l}
                <a
                  class="linkButton"
                  href="/config/automation/edit/${this.automationId}"
                >
                  <mwc-icon-button label="Edit Automation" tabindex="-1">
                    <ha-svg-icon .path=${r.r9}></ha-svg-icon>
                  </mwc-icon-button>
                </a>
              </div>`}
          ${this._traces&&this._traces.length>0?o.dy`
                <div>
                  <mwc-icon-button
                    .disabled=${this._traces[this._traces.length-1].run_id===this._runId}
                    label="Older trace"
                    @click=${this._pickOlderTrace}
                  >
                    <ha-svg-icon .path=${r.JXK}></ha-svg-icon>
                  </mwc-icon-button>
                  <select .value=${this._runId} @change=${this._pickTrace}>
                    ${(0,s.r)(this._traces,(e=>e.run_id),(e=>o.dy`<option value=${e.run_id}>
                          ${(0,d.E)(new Date(e.timestamp.start),this.hass.locale)}
                        </option>`))}
                  </select>
                  <mwc-icon-button
                    .disabled=${this._traces[0].run_id===this._runId}
                    label="Newer trace"
                    @click=${this._pickNewerTrace}
                  >
                    <ha-svg-icon .path=${r.RWP}></ha-svg-icon>
                  </mwc-icon-button>
                </div>
              `:""}
          ${this.narrow?"":o.dy`<div>${h}</div>`}
        </div>

        ${void 0===this._traces?o.dy`<div class="container">Loading…</div>`:0===this._traces.length?o.dy`<div class="container">No traces found</div>`:void 0===this._trace?"":o.dy`
              <div class="main">
                <div class="graph">
                  <hat-script-graph
                    .trace=${this._trace}
                    .selected=${null===(e=this._selected)||void 0===e?void 0:e.path}
                    @graph-node-selected=${this._pickNode}
                  ></hat-script-graph>
                </div>

                <div class="info">
                  <div class="tabs top">
                    ${[["details","Step Details"],["timeline","Trace Timeline"],["logbook","Related logbook entries"],["config","Automation Config"]].map((([e,t])=>o.dy`
                        <button
                          tabindex="0"
                          .view=${e}
                          class=${(0,a.$)({active:this._view===e})}
                          @click=${this._showTab}
                        >
                          ${t}
                        </button>
                      `))}
                    ${this._trace.blueprint_inputs?o.dy`
                          <button
                            tabindex="0"
                            .view=${"blueprint"}
                            class=${(0,a.$)({active:"blueprint"===this._view})}
                            @click=${this._showTab}
                          >
                            Blueprint Config
                          </button>
                        `:""}
                  </div>
                  ${void 0===this._selected||void 0===this._logbookEntries||void 0===n?"":"details"===this._view?o.dy`
                        <ha-trace-path-details
                          .hass=${this.hass}
                          .narrow=${this.narrow}
                          .trace=${this._trace}
                          .selected=${this._selected}
                          .logbookEntries=${this._logbookEntries}
                          .trackedNodes=${n}
                          .renderedNodes=${c}
                        ></ha-trace-path-details>
                      `:"config"===this._view?o.dy`
                        <ha-trace-config
                          .hass=${this.hass}
                          .trace=${this._trace}
                        ></ha-trace-config>
                      `:"logbook"===this._view?o.dy`
                        <ha-trace-logbook
                          .hass=${this.hass}
                          .narrow=${this.narrow}
                          .trace=${this._trace}
                          .logbookEntries=${this._logbookEntries}
                        ></ha-trace-logbook>
                      `:"blueprint"===this._view?o.dy`
                        <ha-trace-blueprint-config
                          .hass=${this.hass}
                          .trace=${this._trace}
                        ></ha-trace-blueprint-config>
                      `:o.dy`
                        <ha-trace-timeline
                          .hass=${this.hass}
                          .trace=${this._trace}
                          .logbookEntries=${this._logbookEntries}
                          .selected=${this._selected}
                          @value-changed=${this._timelinePathPicked}
                        ></ha-trace-timeline>
                      `}
                </div>
              </div>
            `}
      </hass-tabs-subpage>
    `}},{kind:"method",key:"firstUpdated",value:function(e){if(E(I(i.prototype),"firstUpdated",this).call(this,e),!this.automationId)return;const t=new URLSearchParams(location.search);this._loadTraces(t.get("run_id")||void 0)}},{kind:"method",key:"updated",value:function(e){if(E(I(i.prototype),"updated",this).call(this,e),e.get("automationId")&&(this._traces=void 0,this._entityId=void 0,this._runId=void 0,this._trace=void 0,this._logbookEntries=void 0,this.automationId&&this._loadTraces()),e.has("_runId")&&this._runId&&(this._trace=void 0,this._logbookEntries=void 0,this.shadowRoot.querySelector("select").value=this._runId,this._loadTrace()),e.has("automations")&&this.automationId&&!this._entityId){const e=this.automations.find((e=>e.attributes.id===this.automationId));this._entityId=null==e?void 0:e.entity_id}}},{kind:"method",key:"_pickOlderTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e+1].run_id,this._selected=void 0}},{kind:"method",key:"_pickNewerTrace",value:function(){const e=this._traces.findIndex((e=>e.run_id===this._runId));this._runId=this._traces[e-1].run_id,this._selected=void 0}},{kind:"method",key:"_pickTrace",value:function(e){this._runId=e.target.value,this._selected=void 0}},{kind:"method",key:"_pickNode",value:function(e){this._selected=e.detail}},{kind:"method",key:"_loadTraces",value:async function(e){if(this._traces=await(0,h.lj)(this.hass,"automation",this.automationId),this._traces.reverse(),e&&(this._runId=e),this._runId&&!this._traces.some((e=>e.run_id===this._runId))){if(this._runId=void 0,this._selected=void 0,e){const e=new URLSearchParams(location.search);e.delete("run_id"),history.replaceState(null,"",`${location.pathname}?${e.toString()}`)}await(0,u.Ys)(this,{text:"Chosen trace is no longer available"})}!this._runId&&this._traces.length>0&&(this._runId=this._traces[0].run_id)}},{kind:"method",key:"_loadTrace",value:async function(){const e=await(0,h.mA)(this.hass,"automation",this.automationId,this._runId);this._logbookEntries=(0,c.p)(this.hass,"logbook")?await(0,l.sS)(this.hass,e.timestamp.start,e.context.id):[],this._trace=e}},{kind:"method",key:"_downloadTrace",value:function(){const e=document.createElement("a");e.download=`trace ${this._entityId} ${this._trace.timestamp.start}.json`,e.href=`data:application/json;charset=utf-8,${encodeURI(JSON.stringify({trace:this._trace,logbookEntries:this._logbookEntries},void 0,2))}`,e.click()}},{kind:"method",key:"_importTrace",value:function(){const e=prompt("Enter downloaded trace");e&&(localStorage.devTrace=e,this._loadLocalTrace(e))}},{kind:"method",key:"_loadLocalStorageTrace",value:function(){localStorage.devTrace&&this._loadLocalTrace(localStorage.devTrace)}},{kind:"method",key:"_loadLocalTrace",value:function(e){const t=JSON.parse(e);this._trace=t.trace,this._logbookEntries=t.logbookEntries}},{kind:"method",key:"_showTab",value:function(e){this._view=e.target.view}},{kind:"method",key:"_timelinePathPicked",value:function(e){const t=e.detail.value,i=this.shadowRoot.querySelector("hat-script-graph").trackedNodes;i[t]&&(this._selected=i[t])}},{kind:"get",static:!0,key:"styles",value:function(){return[p.Qx,v.b,o.iv`
        .toolbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 20px;
          height: var(--header-height);
          padding: 0 16px;
          background-color: var(--primary-background-color);
          font-weight: 400;
          color: var(--app-header-text-color, white);
          border-bottom: var(--app-header-border-bottom, none);
          box-sizing: border-box;
        }

        .toolbar > * {
          display: flex;
          align-items: center;
        }

        :host([narrow]) .toolbar > * {
          display: contents;
        }

        .main {
          height: calc(100% - 56px);
          display: flex;
          background-color: var(--card-background-color);
        }

        :host([narrow]) .main {
          height: auto;
          flex-direction: column;
        }

        .container {
          padding: 16px;
        }

        .graph {
          border-right: 1px solid var(--divider-color);
          overflow-x: auto;
          max-width: 50%;
        }
        :host([narrow]) .graph {
          max-width: 100%;
        }

        .info {
          flex: 1;
          background-color: var(--card-background-color);
        }

        .linkButton {
          color: var(--primary-text-color);
        }
      `]}}]}}),o.oi)}}]);
//# sourceMappingURL=chunk.3f707a6f6d2a8e9c366d.js.map