document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  document.querySelector('#compose-form').addEventListener('submit', () => send_mail);

  // By default, load the inbox
  load_mailbox('inbox');
});

function show_email(email, mailbox) {
  const div = document.createElement('div');
  div.id = "email";
  div.className = "card-body";
  if (email.read !== true){
    div.style.backgroundColor = "Lightblue";
  }else{
    div.style.backgroundColor = "Lightgreen";  
  }

  const recipient = document.createElement('div');
  recipient.id = "recipient";
  recipient.className = "card-title";
  console.log(`mailbox: ${mailbox}`);

  if(mailbox === "inbox"){
    recipient.innerHTML = email.sender;
  }else {
    recipient.innerHTML = email.recipients;   
  }
  div.append(recipient);

  const subject = document.createElement('div');
  subject.id = "recipient";
  subject.className = "card-text";
  subject.innerHTML = email.subject;
  div.append(subject);
  
  const timestamp = document.createElement('div');
  timestamp.id = "recipient";
  timestamp.className = "card-footer text-muted";
  timestamp.innerHTML = email.timestamp;
  div.append(timestamp);
  var archive = email['archived'];

  var button = document.createElement('button');
  var reply = document.createElement('button');

  if (archive) {
    button.innerText = 'Unarchive';
  }
  else {
    button.innerText = 'Archive';
  }
  reply.innerText = 'Reply';

  button.classList.add('btn-primary');
  button.classList.add('btn');
  reply.classList.add('btn-primary');
  reply.classList.add('btn');

  button.addEventListener('click', () => {
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: !archive
      })
    });

    load_mailbox('inbox');
  });

  reply.addEventListener('click', () => {


    compose_email();

    document.querySelector('#compose-recipients').value = email['sender'];
    document.querySelector('#compose-body').value = `On ${email['timestamp']}, ${email['sender']} wrote: ${email['body']}`;

    if (email['subject'].search('Re:')) {
      document.querySelector('#compose-subject').value = email['subject'];
    }
    else {
      document.querySelector('#compose-subject').value = `Re: ${email['subject']}`;
    }
  });

  if (mailbox !== "sent"){
  div.appendChild(button);
  div.appendChild(reply);
  }
  const emailCard = document.createElement('div');
  emailCard.className = "card text-center";
  emailCard.append(div);

  recipient.addEventListener('click', () => view_email(email.id) );
  subject.addEventListener('click', () => view_email(email.id) );
  timestamp.addEventListener('click', () => view_email(email.id) );
  document.querySelector("#emails-view").append(emailCard);
}

function email_archive(id, state) {
  const newValue = !state;
  
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: body = JSON.stringify(
      {
        archived: newValue
      }
    )
  })
  load_mailbox('inbox');
  window.location.reload();
}

function view_email(id) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  
  fetch(`/emails/${id}`)
  .then(response => response.json() )
  .then(email => {
    email_as_read(id);

    document.querySelector('#email-view-sender').innerHTML = "From: "+email.sender;
    document.querySelector('#email-view-recipients').innerHTML = "To: " +email.recipients;
    document.querySelector('#email-view-subject').innerHTML = "Title: "+email.subject;
    document.querySelector('#email-view-timestamp').innerHTML = email.timestamp;
    document.querySelector('#email-view-body').innerHTML = email.body;

    document.getElementById('reply-email-button').addEventListener('click', () => reply_email(email) );
  });
  email_as_read(id);
  return false;
}

function email_as_read(id) {
  fetch(`/emails/${id}`, {
    method:"PUT",
    body: body = JSON.stringify({
      read: true
    })
  });
}

function reply_email(email) {
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = email.sender;
  if(email.subject.indexOf("Re: ") === -1){
    email.subject = "Re: "+email.subject
  }
  document.querySelector('#compose-subject').value = email.subject;
  document.querySelector('#compose-body').value = `\n On ${email.timestamp} ${email.sender} wrote: \n ${email.body}`;

}


function send_email() {

  var recipients = document.querySelector('#compose-recipients').value;
  var subject = document.querySelector('#compose-subject').value;
  var body = document.querySelector('#compose-body').value;
  if (recipients != '') {
        fetch('/emails', {
          method: 'POST',
          body: JSON.stringify({
            recipients: recipients,
            subject: subject,
            body: body
          })
        })
          .then(response => response.json())
          .then(result => {
            console.log(result);
              load_mailbox('sent');
            }
          );
      }
    }



function compose_email() {

  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  var email_view = document.querySelector('#emails-view');
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  email_view.style.display = 'block';
  email_view.innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      console.log(emails);
      emails.forEach(email => show_email(email, mailbox));
  })
}