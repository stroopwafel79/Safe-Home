// Download the helper library from https://www.twilio.com/docs/node/install
// Your Account Sid and Auth Token from twilio.com/console
const accountSid = 'AC004163108d2c36a528573dbb616efcbd';
const authToken = 'f6d505c1664c7c31bc3d10ba3a363847';
const client = require('twilio')(accountSid, authToken);

client.messages
  .create({
     body: 'This is the ship that made the Kessel Run in fourteen parsecs?',
     from: '+14083594778',
     to: '+15105520442'
   })
  .then(message => console.log(message.sid))
  .done();
