import { App } from './app';

const MAIN_NET = 'https://api.tez.ie/rpc/mainnet';
// const TEST_NET = 'https://hangzhounet.api.tez.ie';
// const TEST_NET = 'https://hangzhou2net.tzkt.io/';
const TEST_NET = 'https://hangzhounet.smartpy.io';
// const SWAP_CONTRACT_DISCONTINUED = 'KT1FgzUUXrWDGjmDW62z22Mq7RUXAe4YjLxU';
const SWAP_CONTRACT = 'KT1LZR4wt2Ws27jKqmhviQxLgJfSkve94VwX';
const TOKEN_A = 0;
const TOKEN_B = 1;
const IPFS_URL_A = 'https://ipfs.io/ipfs/QmQfKgtAsikhFr63koJ1NvzW1yjqJbNPqti6u8Wn9HX9sx';
const IPFS_URL_B = 'https://ipfs.io/ipfs/QmTsabSzifQm9YkNfiVpCo3rSJHC2c2vW6WJLQPzzt3Pn2';
const TRADE_ID = 8;

const app = new App(SWAP_CONTRACT, TEST_NET);
app.init(TOKEN_B, TOKEN_A);
app.setTradeId(TRADE_ID);
app.connectWallet().then((address) => { 
  console.log(`Wallet connected. Your address: ${address}`); 
  setNameTag((address == null ? "?" : address));
});

function setNameTag(tag) {
  const player = document.getElementById('player');
  const myNametag = player.querySelector('.nametag');
  myNametag.setAttribute('text', 'value', tag);
}

function onConnect () {
  console.log(`Networked AFrame: onConnect: ${new Date()}`);
}

function onSceneLoad() {
  // setNameTag();
  // document.querySelector('a-scene').components['networked-scene'].connect();
}

document.addEventListener("DOMContentLoaded", () => {
  console.log('DOMContentLoaded');

  const scene = document.querySelector('a-scene');

  if (scene.hasLoaded) {
    console.log('scene.hasLoaded');
    onSceneLoad();
  } else {
    scene.addEventListener('loaded', onSceneLoad);
  }

  try {
    
    AFRAME.registerComponent('nfta', {
      init: function () {
    
        this.el.addEventListener('click', () => {
          console.log(`${this.el.getAttribute('id')} clicked`);
          this.el.setAttribute('material', 'src', IPFS_URL_A);
          // this.el.emit('clicked'); 
        });
      },
    });

    AFRAME.registerComponent('nftb', {
      init: function () {
    
        this.el.addEventListener('click', () => {
          console.log(`${this.el.getAttribute('id')} clicked`);
          this.el.setAttribute('material', 'src', IPFS_URL_B);
          // this.el.emit('clicked'); 
        });
      },
    });

    AFRAME.registerComponent('propose', {
      init: function () {
    
        this.el.addEventListener('click', () => {
          console.log(`${this.el.getAttribute('id')} clicked`);
          this.el.setAttribute('material', 'color', 'green');
          // this.el.emit('clicked'); 
          app.setTradeProposal(TOKEN_A, TOKEN_B);
          app.initiateSwap();

        });
      },
    });

    AFRAME.registerComponent('confirm', {
      init: function () {
    
        this.el.addEventListener('click', () => {
          console.log(`${this.el.getAttribute('id')} clicked`);
          this.el.setAttribute('material', 'color', 'green');
          app.confirmSwap();
          // this.el.emit('clicked'); 
        });
      },
    });
    
    AFRAME.registerComponent('deny', {
      init: function () {
    
        this.el.addEventListener('click', () => {
          console.log(`${this.el.getAttribute('id')} clicked`);
          this.el.setAttribute('material', 'color', 'red');
          app.cancelSwap();
          // this.el.emit('clicked'); 
        });
      },
    });

    AFRAME.registerComponent('spawn-in-circle', {
      schema: {
        radius: {type: 'number', default: 1}
      },
    
      init: function() {
        var el = this.el;
        var center = el.getAttribute('position');
    
        var angleRad = this.getRandomAngleInRadians();
        var circlePoint = this.randomPointOnCircle(this.data.radius, angleRad);
        var worldPoint = {x: circlePoint.x + center.x, y: center.y, z: circlePoint.y + center.z};
        el.setAttribute('position', worldPoint);
    
        var angleDeg = angleRad * 180 / Math.PI;
        var angleToCenter = -1 * angleDeg + 90;
        var rotationStr = '0 ' + angleToCenter + ' 0';
        el.setAttribute('rotation', rotationStr);
      },
    
      getRandomAngleInRadians: function() {
        return Math.random()*Math.PI*2;
      },
    
      randomPointOnCircle: function (radius, angleRad) {
        x = Math.cos(angleRad)*radius;
        y = Math.sin(angleRad)*radius;
        return {x: x, y: y};
      }
    });
    } catch (error) {
    // component already registered
    }





  // function onConnect () {
  //   console.error('On connected to NAF -', new Date());
  
  //   // Examples of listening to NAF events
  //   document.body.addEventListener('connected', function (evt) {
  //     console.error('connected event. clientId =', evt.detail.clientId);
  //   });
  
  //   document.body.addEventListener('clientConnected', function (evt) {
  //     console.error('clientConnected event. clientId =', evt.detail.clientId);
  //   });
  
  //   document.body.addEventListener('clientDisconnected', function (evt) {
  //     console.error('clientDisconnected event. clientId =', evt.detail.clientId);
  //   });
  
  //   document.body.addEventListener('entityCreated', function (evt) {
  //     console.error('entityCreated event', evt.detail.el);
  //   });
  
  //   document.body.addEventListener('entityRemoved', function(evt) {
  //     console.error('entityRemoved event. Entity networkId =', evt.detail.networkId);
  //   });
  // }

  // NAF.schemas.add({
  //   template: '#avatar-template',
  //   components: [
  //     'position',
  //     'rotation',
  //     {
  //       selector: '.head',
  //       component: 'material',
  //       property: 'color'
  //     }
  //   ]
  // });
  

  

});








