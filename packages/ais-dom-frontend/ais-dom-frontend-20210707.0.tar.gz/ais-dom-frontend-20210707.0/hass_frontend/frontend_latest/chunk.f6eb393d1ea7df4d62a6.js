/*! For license information please see chunk.f6eb393d1ea7df4d62a6.js.LICENSE.txt */
(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[24164],{35854:(e,t,i)=>{"use strict";i.d(t,{G:()=>r,R:()=>s});i(65233);var a=i(21006),o=i(98235);const r={properties:{checked:{type:Boolean,value:!1,reflectToAttribute:!0,notify:!0,observer:"_checkedChanged"},toggles:{type:Boolean,value:!0,reflectToAttribute:!0},value:{type:String,value:"on",observer:"_valueChanged"}},observers:["_requiredChanged(required)"],created:function(){this._hasIronCheckedElementBehavior=!0},_getValidity:function(e){return this.disabled||!this.required||this.checked},_requiredChanged:function(){this.required?this.setAttribute("aria-required","true"):this.removeAttribute("aria-required")},_checkedChanged:function(){this.active=this.checked,this.fire("iron-change")},_valueChanged:function(){void 0!==this.value&&null!==this.value||(this.value="on")}},s=[a.V,o.x,r]},62132:(e,t,i)=>{"use strict";i.d(t,{K:()=>c});i(65233);var a=i(35854),o=i(49075),r=i(84938);const s={_checkedChanged:function(){a.G._checkedChanged.call(this),this.hasRipple()&&(this.checked?this._ripple.setAttribute("checked",""):this._ripple.removeAttribute("checked"))},_buttonStateChanged:function(){r.o._buttonStateChanged.call(this),this.disabled||this.isAttached&&(this.checked=this.active)}},c=[o.B,a.R,s]},32296:(e,t,i)=>{"use strict";i(65233);var a=i(62132),o=i(49075),r=i(9672),s=i(50856),c=i(87529);const n=s.d`<style>
  :host {
    display: inline-block;
    white-space: nowrap;
    cursor: pointer;
    --calculated-paper-checkbox-size: var(--paper-checkbox-size, 18px);
    /* -1px is a sentinel for the default and is replaced in \`attached\`. */
    --calculated-paper-checkbox-ink-size: var(--paper-checkbox-ink-size, -1px);
    @apply --paper-font-common-base;
    line-height: 0;
    -webkit-tap-highlight-color: transparent;
  }

  :host([hidden]) {
    display: none !important;
  }

  :host(:focus) {
    outline: none;
  }

  .hidden {
    display: none;
  }

  #checkboxContainer {
    display: inline-block;
    position: relative;
    width: var(--calculated-paper-checkbox-size);
    height: var(--calculated-paper-checkbox-size);
    min-width: var(--calculated-paper-checkbox-size);
    margin: var(--paper-checkbox-margin, initial);
    vertical-align: var(--paper-checkbox-vertical-align, middle);
    background-color: var(--paper-checkbox-unchecked-background-color, transparent);
  }

  #ink {
    position: absolute;

    /* Center the ripple in the checkbox by negative offsetting it by
     * (inkWidth - rippleWidth) / 2 */
    top: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    width: var(--calculated-paper-checkbox-ink-size);
    height: var(--calculated-paper-checkbox-ink-size);
    color: var(--paper-checkbox-unchecked-ink-color, var(--primary-text-color));
    opacity: 0.6;
    pointer-events: none;
  }

  #ink:dir(rtl) {
    right: calc(0px - (var(--calculated-paper-checkbox-ink-size) - var(--calculated-paper-checkbox-size)) / 2);
    left: auto;
  }

  #ink[checked] {
    color: var(--paper-checkbox-checked-ink-color, var(--primary-color));
  }

  #checkbox {
    position: relative;
    box-sizing: border-box;
    height: 100%;
    border: solid 2px;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    border-radius: 2px;
    pointer-events: none;
    -webkit-transition: background-color 140ms, border-color 140ms;
    transition: background-color 140ms, border-color 140ms;

    -webkit-transition-duration: var(--paper-checkbox-animation-duration, 140ms);
    transition-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  /* checkbox checked animations */
  #checkbox.checked #checkmark {
    -webkit-animation: checkmark-expand 140ms ease-out forwards;
    animation: checkmark-expand 140ms ease-out forwards;

    -webkit-animation-duration: var(--paper-checkbox-animation-duration, 140ms);
    animation-duration: var(--paper-checkbox-animation-duration, 140ms);
  }

  @-webkit-keyframes checkmark-expand {
    0% {
      -webkit-transform: scale(0, 0) rotate(45deg);
    }
    100% {
      -webkit-transform: scale(1, 1) rotate(45deg);
    }
  }

  @keyframes checkmark-expand {
    0% {
      transform: scale(0, 0) rotate(45deg);
    }
    100% {
      transform: scale(1, 1) rotate(45deg);
    }
  }

  #checkbox.checked {
    background-color: var(--paper-checkbox-checked-color, var(--primary-color));
    border-color: var(--paper-checkbox-checked-color, var(--primary-color));
  }

  #checkmark {
    position: absolute;
    width: 36%;
    height: 70%;
    border-style: solid;
    border-top: none;
    border-left: none;
    border-right-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-bottom-width: calc(2/15 * var(--calculated-paper-checkbox-size));
    border-color: var(--paper-checkbox-checkmark-color, white);
    -webkit-transform-origin: 97% 86%;
    transform-origin: 97% 86%;
    box-sizing: content-box; /* protect against page-level box-sizing */
  }

  #checkmark:dir(rtl) {
    -webkit-transform-origin: 50% 14%;
    transform-origin: 50% 14%;
  }

  /* label */
  #checkboxLabel {
    position: relative;
    display: inline-block;
    vertical-align: middle;
    padding-left: var(--paper-checkbox-label-spacing, 8px);
    white-space: normal;
    line-height: normal;
    color: var(--paper-checkbox-label-color, var(--primary-text-color));
    @apply --paper-checkbox-label;
  }

  :host([checked]) #checkboxLabel {
    color: var(--paper-checkbox-label-checked-color, var(--paper-checkbox-label-color, var(--primary-text-color)));
    @apply --paper-checkbox-label-checked;
  }

  #checkboxLabel:dir(rtl) {
    padding-right: var(--paper-checkbox-label-spacing, 8px);
    padding-left: 0;
  }

  #checkboxLabel[hidden] {
    display: none;
  }

  /* disabled state */

  :host([disabled]) #checkbox {
    opacity: 0.5;
    border-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
  }

  :host([disabled][checked]) #checkbox {
    background-color: var(--paper-checkbox-unchecked-color, var(--primary-text-color));
    opacity: 0.5;
  }

  :host([disabled]) #checkboxLabel  {
    opacity: 0.65;
  }

  /* invalid state */
  #checkbox.invalid:not(.checked) {
    border-color: var(--paper-checkbox-error-color, var(--error-color));
  }
</style>

<div id="checkboxContainer">
  <div id="checkbox" class$="[[_computeCheckboxClass(checked, invalid)]]">
    <div id="checkmark" class$="[[_computeCheckmarkClass(checked)]]"></div>
  </div>
</div>

<div id="checkboxLabel"><slot></slot></div>`;n.setAttribute("strip-whitespace",""),(0,r.k)({_template:n,is:"paper-checkbox",behaviors:[a.K],hostAttributes:{role:"checkbox","aria-checked":!1,tabindex:0},properties:{ariaActiveAttribute:{type:String,value:"aria-checked"}},attached:function(){(0,c.T8)(this,(function(){if("-1px"===this.getComputedStyleValue("--calculated-paper-checkbox-ink-size").trim()){var e=this.getComputedStyleValue("--calculated-paper-checkbox-size").trim(),t="px",i=e.match(/[A-Za-z]+$/);null!==i&&(t=i[0]);var a=parseFloat(e),o=8/3*a;"px"===t&&(o=Math.floor(o))%2!=a%2&&o++,this.updateStyles({"--paper-checkbox-ink-size":o+t})}}))},_computeCheckboxClass:function(e,t){var i="";return e&&(i+="checked "),t&&(i+="invalid"),i},_computeCheckmarkClass:function(e){return e?"":"hidden"},_createRipple:function(){return this._rippleContainer=this.$.checkboxContainer,o.S._createRipple.call(this)}})},24734:(e,t,i)=>{"use strict";i.d(t,{B:()=>o});var a=i(47181);const o=(e,t)=>{(0,a.B)(e,"show-dialog",{dialogTag:"dialog-media-player-browse",dialogImport:()=>Promise.all([i.e(78161),i.e(13967),i.e(1041),i.e(91657),i.e(87724),i.e(62613),i.e(59799),i.e(6294),i.e(20839),i.e(58251),i.e(74535),i.e(13997),i.e(95220)]).then(i.bind(i,52809)),dialogParams:t})}},51444:(e,t,i)=>{"use strict";i.d(t,{_:()=>r});var a=i(47181);const o=()=>Promise.all([i.e(75009),i.e(81199),i.e(72420)]).then(i.bind(i,72420)),r=e=>{(0,a.B)(e,"show-dialog",{dialogTag:"ha-voice-command-dialog",dialogImport:o,dialogParams:{}})}},24164:(e,t,i)=>{"use strict";i.r(t);var a=i(50424),o=i(55358),r=(i(39841),i(53268),i(12730),i(32296),i(68644),i(1819),i(51444)),s=i(24734),c=i(47181);i(48932),i(22098);const n={title:"AI-Speaker",views:[{badges:[],cards:[{cards:[{artwork:"full-cover",entity:"media_player.wbudowany_glosnik",hide:{power:!0,runtime:!1,shuffle:!1,source:!0},icon:"mdi:monitor-speaker",more_info:!1,name:" ",shortcuts:{buttons:[{icon:"mdi:bookmark-music",id:"script.ais_add_item_to_bookmarks",type:"script"},{icon:"mdi:thumb-up",id:"script.ais_add_item_to_favorites",type:"script"}],columns:2,list:[]},show_progress:!0,speaker_group:{platform:"ais",show_group_count:!0},tts:{platform:"ais"},type:"ais-mini-media-player"},{type:"conditional",conditions:[{entity:"sensor.ais_gate_model",state:"AIS-PRO1"}],card:{type:"ais-expansion-panel",icon:"mdi:tune",cards:[{entities:[{entity:"input_select.ais_audio_routing"},{entity:"input_boolean.ais_audio_mono"},{entity:"input_number.media_player_speed"}],show_header_toggle:!1,type:"entities"}]}},{cards:[{cards:[{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:heart",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"ais_favorites"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ulubione"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:bookmark",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"ais_bookmarks"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"zakładki"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:monitor-speaker",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"ais_tv"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:folder",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"local_audio"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"dyski"}},type:"ais-button"}],type:"horizontal-stack"},{cards:[{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:radio",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"radio_player"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"radio"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:podcast",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"podcast_player"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"podcast"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:book-music",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"audiobooks_player"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"audiobook"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_player_mode",icon:"mdi:music",name:" ",show_state:!1,size:"30%",state:[{color:"var(--primary-color)",value:"music_player"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"muzyka"}},type:"ais-button"}],type:"horizontal-stack"}],type:"vertical-stack"},{content:"{{ states.sensor.aisknowledgeanswer.attributes.text }}\n",type:"markdown"},{card:{cards:[{cards:[{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_mode",icon:"mdi:monitor-dashboard",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"tv_on"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_on"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_mode",icon:"mdi:television-off",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"tv_off"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_off"}},type:"ais-button"}],type:"horizontal-stack"},{card:{cards:[{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_activity",icon:"mdi:youtube-tv",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"youtube"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_youtube"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_activity",icon:"mdi:spotify",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"spotify"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_spotify"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_activity",icon:"mdi:cctv",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"camera"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_cameras"}},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"sensor.ais_tv_activity",icon:"mdi:tune-variant",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"settings"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_settings"}},type:"ais-button"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_tv_mode",state:"tv_on"}],type:"conditional"},{card:{cards:[{card:{type:"glance",columns:3,show_state:!1},filter:{include:[{domain:"camera",options:{tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"ais_tv_show_camera",entity_id:"this.entity_id"}}}}]},type:"ais-auto-entities"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_tv_activity",state:"camera"}],type:"conditional"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"ais_tv"}],type:"conditional"},{card:{cards:[{cards:[{color:"#727272",color_type:"icon",entity:"input_select.ais_music_service",icon:"mdi:youtube",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"YouTube"}],tap_action:{action:"call-service",service:"ais_cloud.change_audio_service"},type:"ais-button"},{color:"#727272",color_type:"icon",entity:"input_select.ais_music_service",icon:"mdi:spotify",name:" ",show_state:!1,size:"12%",state:[{color:"var(--primary-color)",value:"Spotify"}],tap_action:{action:"call-service",service:"ais_cloud.change_audio_service"},type:"ais-button"}],type:"horizontal-stack"},{card:{cards:[{entities:[{entity:"input_text.ais_music_query"}],show_header_toggle:!1,title:"Wyszukiwanie Muzyki",type:"entities"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"YouTube"}],type:"conditional"},{card:{cards:[{entities:[{entity:"input_text.ais_spotify_query"}],show_header_toggle:!1,title:"Wyszukiwanie Muzyki",type:"entities"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],type:"conditional"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"}],type:"conditional"},{cards:[{card:{show_header_toggle:!1,type:"entities"},filter:{include:[{domain:"media_player"}]},type:"ais-auto-entities"}],icon:"mdi:speaker-multiple",type:"ais-expansion-panel"},{card:{cards:[{entity:"input_select.book_autor",type:"ais-easy-picker"}],type:"vertical-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"audiobooks_player"}],type:"conditional"}],show_header_toggle:!1,type:"vertical-stack"},{cards:[{card:{entity:"sensor.ais_drives",title:"Przeglądanie Dysków",type:"ais-files-list"},conditions:[{entity:"sensor.ais_player_mode",state:"local_audio"}],type:"conditional"},{card:{entity:["sensor.aisbookmarkslist"],media_source:"Bookmark",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"ais_bookmarks"}],type:"conditional"},{card:{entity:["sensor.aisfavoriteslist"],media_source:"Favorite",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"ais_favorites"}],type:"conditional"},{card:{entity:["sensor.youtubelist"],media_source:"Music",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"YouTube"}],type:"conditional"},{card:{cards:[{icon:"mdi:folder-music",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"featured-playlists"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"featured-playlists"}},type:"ais-button"},{icon:"mdi:playlist-music",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"playlists"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"playlists"}},type:"ais-button"},{icon:"mdi:account",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"artists"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"artists"}},type:"ais-button"},{icon:"mdi:album",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"albums"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"albums"}},type:"ais-button"},{icon:"mdi:music-note",entity:"sensor.ais_spotify_favorites_mode",show_name:!1,state:[{color:"var(--primary-color)",value:"tracks"}],tap_action:{action:"call-service",service:"ais_spotify_service.get_favorites",service_data:{type:"tracks"}},type:"ais-button"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],type:"conditional"},{card:{entity:["sensor.spotifysearchlist"],media_source:"SpotifySearch",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],type:"conditional"},{card:{cards:[{icon:"mdi:account",entity:"sensor.ais_radio_origin",show_name:!0,name:"Moje",state:[{color:"var(--primary-color)",value:"private"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"radio_private"}},type:"ais-button"},{icon:"mdi:earth",entity:"sensor.ais_radio_origin",show_name:!0,name:"Publiczne",state:[{color:"var(--primary-color)",value:"public"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"radio_public"}},type:"ais-button"},{icon:"mdi:share-variant",entity:"sensor.ais_radio_origin",show_name:!0,name:"Udostępnione",state:[{color:"var(--primary-color)",value:"shared"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"radio_shared"}},type:"ais-button"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"}],type:"conditional"},{card:{entity:"input_select.radio_type",type:"ais-easy-picker",orgin:"public"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"},{entity:"sensor.ais_radio_origin",state:"public"}],type:"conditional"},{card:{entity:"input_select.radio_type",type:"ais-easy-picker",orgin:"private"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"},{entity:"sensor.ais_radio_origin",state:"private"}],type:"conditional"},{card:{entity:"input_select.radio_type",type:"ais-easy-picker",orgin:"shared"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"},{entity:"sensor.ais_radio_origin",state:"shared"}],type:"conditional"},{card:{cards:[{icon:"mdi:account",entity:"sensor.ais_podcast_origin",show_name:!0,name:"Moje",state:[{color:"var(--primary-color)",value:"private"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"podcast_private"}},type:"ais-button"},{icon:"mdi:earth",entity:"sensor.ais_podcast_origin",show_name:!0,name:"Publiczne",state:[{color:"var(--primary-color)",value:"public"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"podcast_public"}},type:"ais-button"},{icon:"mdi:share-variant",entity:"sensor.ais_podcast_origin",show_name:!0,name:"Udostępnione",state:[{color:"var(--primary-color)",value:"shared"}],tap_action:{action:"call-service",service:"ais_ai_service.set_context",service_data:{text:"podcast_shared"}},type:"ais-button"}],type:"horizontal-stack"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"}],type:"conditional"},{card:{entity:"input_select.podcast_type",type:"ais-easy-picker",orgin:"public"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"},{entity:"sensor.ais_podcast_origin",state:"public"}],type:"conditional"},{card:{entity:"input_select.podcast_type",type:"ais-easy-picker",orgin:"private"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"},{entity:"sensor.ais_podcast_origin",state:"private"}],type:"conditional"},{card:{entity:"input_select.podcast_type",type:"ais-easy-picker",orgin:"shared"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"},{entity:"sensor.ais_podcast_origin",state:"shared"}],type:"conditional"},{card:{entity:["sensor.podcastnamelist"],media_source:"PodcastName",type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"}],type:"conditional"},{card:{entity:["sensor.audiobookslist"],media_source:"AudioBook",type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"audiobooks_player"}],type:"conditional"}],type:"vertical-stack"},{cards:[{card:{entity:["sensor.spotifylist"],media_source:"Spotify",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"music_player"},{entity:"input_select.ais_music_service",state:"Spotify"}],type:"conditional"},{card:{entity:["sensor.radiolist"],media_source:"Radio",show_delete_icon:!0,type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"radio_player"}],type:"conditional"},{card:{entity:["sensor.podcastlist"],media_source:"Podcast",type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"podcast_player"}],type:"conditional"},{card:{entity:["sensor.audiobookschapterslist"],media_source:"AudioBookChapter",type:"ais-list"},conditions:[{entity:"sensor.ais_player_mode",state:"audiobooks_player"}],type:"conditional"}],type:"vertical-stack"}],icon:"mdi:music",path:"aisaudio",title:"Audio",visible:!1}]};i(71743);var l=i(11654);function d(){d=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(a){t.forEach((function(t){var o=t.placement;if(t.kind===a&&("static"===o||"prototype"===o)){var r="static"===o?e:i;this.defineClassElement(r,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var a=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===a?void 0:a.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],a=[],o={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,o)}),this),e.forEach((function(e){if(!_(e))return i.push(e);var t=this.decorateElement(e,o);i.push(t.element),i.push.apply(i,t.extras),a.push.apply(a,t.finishers)}),this),!t)return{elements:i,finishers:a};var r=this.decorateConstructor(i,t);return a.push.apply(a,r.finishers),r.finishers=a,r},addElementPlacement:function(e,t,i){var a=t[e.placement];if(!i&&-1!==a.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");a.push(e.key)},decorateElement:function(e,t){for(var i=[],a=[],o=e.decorators,r=o.length-1;r>=0;r--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var c=this.fromElementDescriptor(e),n=this.toElementFinisherExtras((0,o[r])(c)||c);e=n.element,this.addElementPlacement(e,t),n.finisher&&a.push(n.finisher);var l=n.extras;if(l){for(var d=0;d<l.length;d++)this.addElementPlacement(l[d],t);i.push.apply(i,l)}}return{element:e,finishers:a,extras:i}},decorateConstructor:function(e,t){for(var i=[],a=t.length-1;a>=0;a--){var o=this.fromClassDescriptor(e),r=this.toClassDescriptor((0,t[a])(o)||o);if(void 0!==r.finisher&&i.push(r.finisher),void 0!==r.elements){e=r.elements;for(var s=0;s<e.length-1;s++)for(var c=s+1;c<e.length;c++)if(e[s].key===e[c].key&&e[s].placement===e[c].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),a=String(e.placement);if("static"!==a&&"prototype"!==a&&"own"!==a)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+a+'"');var o=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var r={kind:t,key:i,placement:a,descriptor:Object.assign({},o)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(o,"get","The property descriptor of a field descriptor"),this.disallowProperty(o,"set","The property descriptor of a field descriptor"),this.disallowProperty(o,"value","The property descriptor of a field descriptor"),r.initializer=e.initializer),r},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:h(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=h(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var a=(0,t[i])(e);if(void 0!==a){if("function"!=typeof a)throw new TypeError("Finishers must return a constructor.");e=a}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function p(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var a={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(a.decorators=e.decorators),"field"===e.kind&&(a.initializer=e.value),a}function y(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function _(e){return e.decorators&&e.decorators.length}function u(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function h(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var a=i.call(e,t||"default");if("object"!=typeof a)return a;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,a=new Array(t);i<t;i++)a[i]=e[i];return a}!function(e,t,i,a){var o=d();if(a)for(var r=0;r<a.length;r++)o=a[r](o);var s=t((function(e){o.initializeInstanceElements(e,c.elements)}),i),c=o.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===r.key&&e.placement===r.placement},a=0;a<e.length;a++){var o,r=e[a];if("method"===r.kind&&(o=t.find(i)))if(u(r.descriptor)||u(o.descriptor)){if(_(r)||_(o))throw new ReferenceError("Duplicated methods ("+r.key+") can't be decorated.");o.descriptor=r.descriptor}else{if(_(r)){if(_(o))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+r.key+").");o.decorators=r.decorators}y(r,o)}else t.push(r)}return t}(s.d.map(p)),e);o.initializeClassElements(s.F,c.elements),o.runClassFinishers(s.F,c.finishers)}([(0,o.Mo)("ha-panel-aisaudio")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.Cb)({type:Boolean,reflect:!0})],key:"narrow",value:void 0},{kind:"method",key:"_showBrowseMedia",value:function(){(0,s.B)(this,{action:"play",entityId:"media_player.wbudowany_glosnik",mediaPickedCallback:e=>this.hass.callService("media_player","play_media",{entity_id:"media_player.wbudowany_glosnik",media_content_id:e.item.media_content_id,media_content_type:e.item.media_content_type})})}},{kind:"method",key:"_showCheckAisMedia",value:function(){var e,t;e=this,t={selectedOptionCallback:e=>console.log("option: "+e)},(0,c.B)(e,"show-dialog",{dialogTag:"hui-dialog-check-media-source-ais",dialogImport:()=>Promise.all([i.e(78161),i.e(13967),i.e(87724),i.e(62613),i.e(75682)]).then(i.bind(i,19778)),dialogParams:t})}},{kind:"method",key:"_showAddAisMedia",value:function(){var e,t;e=this,t={selectedOptionCallback:e=>console.log("option: "+e)},(0,c.B)(e,"show-dialog",{dialogTag:"hui-dialog-add-media-source-ais",dialogImport:()=>Promise.all([i.e(78161),i.e(13967),i.e(87724),i.e(62613),i.e(30149),i.e(9533),i.e(854)]).then(i.bind(i,32205)),dialogParams:t})}},{kind:"method",key:"_showVoiceCommandDialog",value:function(){(0,r._)(this)}},{kind:"method",key:"render",value:function(){const e={config:n,rawConfig:n,editMode:!1,urlPath:null,enableFullEditMode:()=>{},mode:"storage",locale:this.hass.locale,saveConfig:async()=>{},deleteConfig:async()=>{},setEditMode:()=>{}};return a.dy`
      <app-header-layout has-scrolling-region>
        <app-header fixed slot="header">
          <app-toolbar>
            <ha-menu-button
              .hass=${this.hass}
              .narrow=${this.narrow}
            ></ha-menu-button>
            <ha-icon-button
              label="Informacje o audio"
              icon="hass:information"
              @click=${this._showCheckAisMedia}
            ></ha-icon-button>
            <ha-icon-button
              label="Dodaj audio"
              icon="hass:music-note-plus"
              @click=${this._showAddAisMedia}
            ></ha-icon-button>
            <div main-title>Audio</div>
            <ha-icon-button
              label="Przeglądaj media"
              icon="hass:folder-multiple"
              @click=${this._showBrowseMedia}
            ></ha-icon-button>
            <ha-icon-button
              label="Rozpocznij rozmowę"
              icon="hass:forum-outline"
              @click=${this._showVoiceCommandDialog}
            ></ha-icon-button>
          </app-toolbar>
        </app-header>
        <hui-view .hass=${this.hass} .lovelace=${e} index="0"></hui-view>
      </app-header-layout>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return[l.Qx,a.iv`
        :host {
          min-height: 100vh;
          height: 0;
          display: flex;
          flex-direction: column;
          box-sizing: border-box;
          background: var(--primary-background-color);
        }
        :host > * {
          flex: 1;
        }
      `]}}]}}),a.oi)}}]);
//# sourceMappingURL=chunk.f6eb393d1ea7df4d62a6.js.map