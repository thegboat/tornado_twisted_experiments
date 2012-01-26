String.prototype.lstrip = function(){
  return this.replace(/^\s+/,'')
}

String.prototype.rstrip = function(){
  return  this.replace(/\s+$/,'')
}

String.prototype.strip = function(){
  var temp = this.rstrip()
  return temp.lstrip()
}

String.prototype.blank = function(){
  return !this.replace(/\s+/g,'')
}

String.prototype.humanize = function(){
  var list = this.strip().split('_')
  first = list[0][0].toUpperCase() + list[0].substr(1,list[0].length)
  list = [first].concat(list.slice(1,list.length))
  return list.join(' ').replace(/\s+/g,' ')
}

String.prototype.valid_email = function(){
  return /^([^@\s]+)@((?:[-a-z0-9]+\.)+[a-z]{2,6})$/i.test(this)
}

String.prototype.valid_phone = function(){
  return this.replace(/\D/g,'').length > 9 && this.replace(/\D/g,'').length < 14
}

String.prototype.include = function(x){
  return this.indexOf(x) > -1
}

String.prototype.date = function(){
  if ((/^\d{4}-\d{2}-[0-3]{1}\d{1}T[0-2]{1}\d{1}:[0-5]\d{1}:[0-5]\d{1}[A-Z]{1}$/).test(this)){
    var tmp = this.replace(/\s+/,'').substring(0,this.length - 1)
    var date = tmp.split('T')[0], time = tmp.split('T')[1]
    var year = date.split('-')[0]
    var month = date.split('-')[1]
    var day = date.split('-')[2]
    var hour = time.split(':')[0]
    var min = time.split(':')[1]
    var sec = time.split(':')[2]
    return new Date(year,month,day,hour,min,sec)
  }
  return null
}

Array.prototype.empty = function(){
  return this.length == 0
}

Array.prototype.include = function(x){
  return this.indexOf(x) > -1
}

Array.prototype.all_like = function(x){
  var res = true
  for(var i=0;i<this.length;i++){
    if (!this[i] || !x.test(String(this[i]))){res = false; break;}
  }
  return res
}

Array.prototype.all_integers = function(){
  return this.all_like(/\d+/)
}


/* custom */
String.prototype.valid_password = function(){
  return /\S{6,}/.test(this.strip())
}