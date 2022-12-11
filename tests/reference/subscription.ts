import {strict} from 'assert'
const baretest = require('baretest')
import {TestScheduler} from 'rxjs/testing'
import { SubscriptionStatusMessage } from '../orderbook'
import { replaceAltCodesOperator } from '../subscription'

export default function(test: typeof baretest, assert: typeof strict) {
  test('replaces XBT with BTC', function() {
    const source =  '---a-----b----'
    const out =     '---0-----1----'
    new TestScheduler((actual, expected) => assert.deepEqual(actual, expected)).run(
      ({cold, expectObservable}) => {
        expectObservable(
          cold(source, {
            a: {pair: 'XBT/BUSD'} as SubscriptionStatusMessage,
            b: {pair: 'LTC/EUR'} as SubscriptionStatusMessage
          }).pipe(
            replaceAltCodesOperator
          )
        ).toBe(
          out, [
            {pair: 'BTC/BUSD'}, 
            {pair: 'LTC/EUR'}
          ]
        )
      }
    )
  })
}