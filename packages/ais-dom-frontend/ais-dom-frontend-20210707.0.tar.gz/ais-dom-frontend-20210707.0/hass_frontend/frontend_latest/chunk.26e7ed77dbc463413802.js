(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6169],{6169:(e,t,s)=>{"use strict";s.r(t);var r=s(50424),i=s(50467),o=s(99476);const n={1:5,2:3,3:2};class a extends o.p{static async getConfigElement(){return await Promise.all([s.e(75009),s.e(78161),s.e(42955),s.e(1041),s.e(91657),s.e(87724),s.e(62613),s.e(68644),s.e(59799),s.e(6294),s.e(4268),s.e(93098),s.e(98595),s.e(56087),s.e(46363),s.e(89266),s.e(15225),s.e(73401),s.e(81480),s.e(87482),s.e(74535),s.e(68331),s.e(68101),s.e(36902),s.e(60033),s.e(18900),s.e(33902),s.e(66442),s.e(52231),s.e(74513),s.e(34475)]).then(s.bind(s,22382)),document.createElement("hui-grid-card-editor")}async getCardSize(){if(!this._cards||!this._config)return 0;if(this.square){const e=n[this.columns]||1;return(this._cards.length<this.columns?e:this._cards.length/this.columns*e)+(this._config.title?1:0)}const e=[];for(const t of this._cards)e.push((0,i.N)(t));const t=await Promise.all(e);let s=this._config.title?1:0;for(let e=0;e<t.length;e+=this.columns)s+=Math.max(...t.slice(e,e+this.columns));return s}get columns(){var e;return(null===(e=this._config)||void 0===e?void 0:e.columns)||3}get square(){var e;return!1!==(null===(e=this._config)||void 0===e?void 0:e.square)}setConfig(e){super.setConfig(e),this.style.setProperty("--grid-card-column-count",String(this.columns)),this.toggleAttribute("square",this.square)}static get styles(){return[super.sharedStyles,r.iv`
        #root {
          display: grid;
          grid-template-columns: repeat(
            var(--grid-card-column-count, ${3}),
            minmax(0, 1fr)
          );
          grid-gap: var(--grid-card-gap, 8px);
        }
        :host([square]) #root {
          grid-auto-rows: 1fr;
        }
        :host([square]) #root::before {
          content: "";
          width: 0;
          padding-bottom: 100%;
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }

        :host([square]) #root > *:first-child {
          grid-row: 1 / 1;
          grid-column: 1 / 1;
        }
      `]}}customElements.define("hui-grid-card",a)}}]);
//# sourceMappingURL=chunk.26e7ed77dbc463413802.js.map