# the swap

A playful interaction in the metaverse.

### How to use for development

Dependencies: [node.js](https://nodejs.org/en/), 2 Tezos accounts on Hangzhounet Testnet

To install dependencies, run: `npm install`.
Then run: `npm run watch`. This auto-generates the output in `dist`.
To serve the folder `dist`, then run: `npm run start`. 

For local testing, you can control both players:

1. Open http://localhost:8080/. Both player views are shown side by side in two iFrames within one browser window. Click in one frame then move the player. 
2. When the two wallet connections pop up, connect **two different accounts on the Hangzhounet Testnet**.

The two NFTs we minted on Testnet as SWP Tokens are also available as OBJKTs on Mainnet, created for developing and testing web 3 applications: 

* pink: https://hicetnunc.art/objkt/589276
* cyan https://hicetnunc.art/objkt/589279 

To test one scene in one window, replace `index.html` with `scene.html`.

To host on a public server, follow the advice here: 
https://github.com/networked-aframe/networked-aframe/blob/master/docs/hosting-networked-aframe-on-a-server.md

### Libraries / Frameworks / Tools: 

* [A-Frame](https://aframe.io/)
* [Networked A-Frame](https://github.com/networked-aframe/networked-aframe)
* [Taquito](https://tezostaquito.io/)
* [Parcel](https://parceljs.org/)
* [SmartPy](https://smartpy.io/)

Made by [jagracar](https://twitter.com/jagracar) (smart contracts) and [crcdng](https://twitter.com/crcdng) (interaction / api).
