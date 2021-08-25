function encodeBase64FromBytes(bytes) {
  var encoder = Java.type('java.util.Base64')
    .getUrlEncoder()
    .withoutPadding()
  return new java.lang.String(encoder.encode(bytes))
}

function encodeBase64(str) {
  return encodeBase64FromBytes(str.getBytes("UTF-8"))
}

function generateJWT(payload, key) {
  var alg = 'HmacSHA256'
  var headerEncoded = encodeBase64(JSON.stringify({ alg: 'HS256', typ: 'JWT' }))
  var payloadEncoded = encodeBase64(JSON.stringify(payload))
  var toSign = headerEncoded + '.' + payloadEncoded
  var sha256HMAC = Java.type('javax.crypto.Mac').getInstance(alg)
  var secretKey = new javax.crypto.spec.SecretKeySpec(key.getBytes('UTF-8'), alg)
  sha256HMAC.init(secretKey)
  var signature = encodeBase64FromBytes(sha256HMAC.doFinal(toSign.getBytes('UTF-8')))
  var token = toSign + '.' + signature
  return token
}

return {
  encode: generateJWT,
};