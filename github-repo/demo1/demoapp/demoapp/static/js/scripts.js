
// signup form jquery to confirm if the email id does not exist 
$("form[name=signup_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/signup",
    type: "POST",
    data: data,
    dataType: "json",
    success: function(resp) {
      document.getElementById("p1").innerHTML = "welcome you are logged!";
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });
  e.preventDefault();
});

// login form jquery to check if the user is already registered and check password
$("form[name=login_form").submit(function(e) {

  var $form = $(this);
  var $error = $form.find(".error");
  var data = $form.serialize();

  $.ajax({
    url: "/user/login",
    type: "POST",
    data: data,
    dataType: "json",
   
    success: function(resp) {
      console.log(data +" ssssssssssssssssssssssssssssssss");
      document.getElementById("p1").innerHTML = "New tttttext!";
      window.location.href = "/dashboard/";
    },
    error: function(resp) {
      console.log("eeeeeeeeeeeeeeeeeeeeeeeeeeeeeee");
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
    }
  });

  e.preventDefault();
});

// sends and recives messages from bot
$(document).ready(function(){
  $("form[name=message_form").submit(function(e) {
    var $form = $(this);
    var $messages = $form.find("#message_box");
    var data = $form.serialize();


    var fwd_remote='<article class="msg-container msg-remote" id="msg-0"> <div class="msg-box"><div class="flr"><div class="messages"><p class="msg" id="msg-0">'
       ,bwd_remote='</p></div><span class="timestamp">&bull;<span class="username">GreetingsBot</span></span></div></div></article>'
       ,fwd_self='<article class="msg-container msg-self" id="msg-0"><div class="msg-box"><div class="flr"><div class="messages"><p class="msg" id="msg-1">'
       ,bwd_self='</p></div><span class="timestamp">&bull;<span class="username">You</span></span></div></div></article>'
       ;

    dataa={}
    $form.find( '[name]' ).each( function( i , v ){
      var input = $( this ), // resolves to current input element.
          name = input.attr( 'name' ),
          value = input.val();
      dataa[name] = value;
    });
    console.log(dataa+" "+dataa['message']+" "+dataa['test']);

    //appending user message to the messagebox
    $('#message_box').append(fwd_self+dataa['message']+bwd_self);
    
    $.ajax({
      url: "/ChatterBot/get_response",
      type: "POST",
      data: data,
      dataType: "json",
      success: function(resp) {
        console.log(resp+" "+resp['reply']+" "+resp['bot']);
        if(resp){
    //appending responses of the bot to the message_box
						$('#message_box').append(fwd_remote+resp['reply']+bwd_remote);
				}
        $('#message').val('');
				document.getElementById('chat-window').scrollTop = document.getElementById('chat-window').scrollHeight;
      }
    });
    e.preventDefault();
  });
});
