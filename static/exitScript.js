function exitOnProfile() {
    document.cookie = 'token=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
    document.location.href = '/'
  }