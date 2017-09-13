PWA Offline License(Persistent option)
---

<h3>Shaka Player</h3>
****
* Drm info에 persistentStateRequired를 true로 한다. 다만 이것은 오프라인 라이선스 지원을 허가한다는 의미가 아니다.

<pre><code>   static wrapDRMInfo (name, url) {
    console.log(name + ":::" + url);
    function base64DecodeUint8Array(input) {
      var raw = window.atob(input);
      var rawLength = raw.length;
      var array = new Uint8Array(new ArrayBuffer(rawLength));

      for(var i = 0; i < rawLength; i++)
        array[i] = raw.charCodeAt(i);

      return array;
    }

    let base64Cert = '[cert data]';
    let serverCertificate = base64DecodeUint8Array(base64Cert);

    if (!name) {
      return;
    }

    const drm = {
      servers: {
        'com.widevine.alpha': 'license server url',
      },
      advanced: {
        'com.widevine.alpha': {
          'persistentStateRequired':true,
          'serverCertificate': serverCertificate
        }
      }
    };

    drm.servers[name] = url;
    return drm;
  }</code></pre>

* 위와 같은 설정으로 라이선스를 발급한다. desktop chrome에서 발급 시도시 "licenseType":"STREAMING" 로 옵션이 설정됨. 이건 해결해야함.

<pre><code>  static get CONTENT_FORMAT () {
    return 'cenc';
  }

  static get CONTENT_TYPE () {
    return 'video/mp4;codecs="avc1.4d401e"';
  }

  static get AUDIO_CONFIG(){
    return 'audio/mp4;codecs="mp4a.40.2"';
  }

  static get CONFIG () {
    return [{
      initDataTypes: [LicensePersister.CONTENT_FORMAT]
      ,audioCapabilities: [
        {
          contentType:LicensePersister.AUDIO_CONFIG
          ,robustness:"SW_SECURE_CRYPTO"
        }]
      ,videoCapabilities: [
        {
          contentType:LicensePersister.CONTENT_TYPE
          ,robustness:"SW_SECURE_CRYPTO"
        }]
      ,persistentState: 'required'
      //TODO persistent-license 지원 필요
      ,sessionTypes: ['persistent-license']
    }];
  }</code></pre>

위의 옵션을 적용하여 navigator.requestMediaKeySystemAccess(name, config)를 호출한다. 여기서 name은 widevine를 사용하기 때문에 com.widevine.alpha으로 세팅해야함.

<pre><code>navigator.requestMediaKeySystemAccess(name, config)
  .then(keySystemAccess => {
    return keySystemAccess.createMediaKeys();
  }).then(createdMediaKeys => {
    return createdMediaKeys.createSession('persistent-license');
  })</code></pre>

주의사항
---
* 위와 같이 오프라인 라이선스를 사용할때 DRM별로 오프라인 라이선스 지원 여부를 파악해야한다. widevine같은 경우는 스펙상 오프라인 라이선스를 지원하지만, desktop chrome의 경우는 지원하지 않는다. mobile chrome, chromebook에 한하여 지원한다.
