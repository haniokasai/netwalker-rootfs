��    8      �  O   �      �  �  �  �  �  �  -
  
  �  N  �  �   3  _      m  �  v  �  P  ]  �    C  t  H   /  �#  K  �&  C  9+    }.  '  �1  6  �5    �8  �  <  '  @  �  +C  �  �F  �  �J  n  N  @  �R  �  �U  T  cY  5  �]  �  �a  I  �e  �  +i  �  �l  �  �p  �  �s  �  ww  8  Kz  2  �}  �  ��  �  �  �  2�  �  ڋ  �  ��  �  {�    G�  �  S�  �  �    ͝  �  �  (  ��  �  �  �   ��  �  t�  �  e�  �  G�  �  ׭  �   ��  �  ��  �   2�  P  /�  �   ��  _  [�  �   ��  �   ��  �  ~�  _  �  �   u�  u  A�  0  ��  K  ��  C  4�    x�  '  ��  6  ��    ��  �  �  '  ��  �  &�  �  ��  �  ��  n  �  @  ��  �  ��  T  ^  5  � �  � I  � �  & �  � �  � �  � �  r 8  F! 2  $ �  �( �  {+ �  // �  �2 �  �5 �  f8   ; �  > �  �?   �D �  �F *  �I �  �J �   yL �  >M �  1P       6         "          +           1                          	          &             %       ,      *       .   -                     5   (   #   3   '                       
         8                2   !                0   )   4                          7   $   /                @FUNCTION=ACCRINTM
@SYNTAX=ACCRINTM(issue,maturity,rate[,par,basis])
@DESCRIPTION=ACCRINTM calculates and returns the accrued interest for a security from @issue to @maturity date.

@issue is the issue date of the security.  @maturity is the maturity date of the security.  @rate is the annual rate of the security and @par is the par value of the security. If you omit @par, ACCRINTM applies $1,000 instead.  @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @issue date or @maturity date is not valid, ACCRINTM returns #NUM! error.
* If @rate <= 0 or @par <= 0, ACCRINTM returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, ACCRINTM returns #NUM! error.
* If @issue date is after @maturity date or they are the same, ACCRINTM returns #NUM! error.

@EXAMPLES=

@SEEALSO=ACCRINT @FUNCTION=BASE
@SYNTAX=BASE(number,base[,length])
@DESCRIPTION=BASE function converts a number to a string representing that number in base @base.

* @base must be an integer between 2 and 36.
* This function is OpenOffice.Org compatible.
* Optional argument @length specifies the minimum result length.  Leading  zeroes will be added to reach this length.

@EXAMPLES=
BASE(255,16,4) equals "00FF".

@SEEALSO=DECIMAL @FUNCTION=CEILING
@SYNTAX=CEILING(x[,significance])
@DESCRIPTION=CEILING function rounds @x up to the nearest multiple of @significance.

* If @x or @significance is non-numeric CEILING returns #VALUE! error.
* If @x and @significance have different signs CEILING returns #NUM! error.
* This function is Excel compatible.

@EXAMPLES=
CEILING(2.43,1) equals 3.
CEILING(123.123,3) equals 126.

@SEEALSO=CEIL, FLOOR, ABS, INT, MOD @FUNCTION=DECIMAL
@SYNTAX=DECIMAL(text,base)
@DESCRIPTION=DECIMAL function converts a number in base @base to decimal.

* @base must be an integer between 2 and 36.
* This function is OpenOffice.Org compatible.

@EXAMPLES=
DECIMAL("A1",16) equals 161.

@SEEALSO=BASE @FUNCTION=DISC
@SYNTAX=DISC(settlement,maturity,par,redemption[,basis])
@DESCRIPTION=DISC calculates and returns the discount rate for a security. @settlement is the settlement date of the security.

@maturity is the maturity date of the security.  @par is the price per $100 face value of the security.  @redemption is the redemption value per $100 face value of the security.

@basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @settlement date or @maturity date is not valid, DISC returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, DISC returns #NUM! error.
* If @settlement date is after @maturity date or they are the same, DISC returns #NUM! error.

@EXAMPLES=

@SEEALSO= @FUNCTION=DOLLAR
@SYNTAX=DOLLAR(num[,decimals])
@DESCRIPTION=DOLLAR returns @num formatted as currency.

* This function is Excel compatible.

@EXAMPLES=
DOLLAR(12345) equals "$12,345.00".

@SEEALSO=FIXED, TEXT, VALUE @FUNCTION=DURATION
@SYNTAX=DURATION(settlement,maturity,coup,yield,frequency[,basis])
@DESCRIPTION=DURATION calculates the duration of a security.

@settlement is the settlement date of the security.
@maturity is the maturity date of the security.
@coup The annual coupon rate as a percentage.
@yield The annualized yield of the security as a percentage.
@frequency is the number of coupon payments per year. Allowed frequencies are: 1 = annual, 2 = semi, 4 = quarterly. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, DURATION returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO=G_DURATION,MDURATION @FUNCTION=EVEN
@SYNTAX=EVEN(number)
@DESCRIPTION=EVEN function returns the number rounded up to the nearest even integer.  Negative numbers are rounded down.

* This function is Excel compatible.
 
@EXAMPLES=
EVEN(5.4) equals 6.
EVEN(-5.4) equals -6.

@SEEALSO=ODD @FUNCTION=EXPPOWDIST
@SYNTAX=EXPPOWDIST(x,a,b)
@DESCRIPTION=EXPPOWDIST returns the probability density p(x) at @x for Exponential Power distribution with scale parameter @a and exponent @b.
This distribution has been recommended for lifetime analysis when a U-shaped hazard function is desired. This corresponds to rapid failure once the product starts to wear out after a period of steady or even improving reliability.
@EXAMPLES=
EXPPOWDIST(0.4,1,2).

@SEEALSO=RANDEXPPOW @FUNCTION=INTRATE
@SYNTAX=INTRATE(settlement,maturity,investment,redemption[,basis])
@DESCRIPTION=INTRATE calculates and returns the interest rate of a fully vested security.

@settlement is the settlement date of the security.  @maturity is the maturity date of the security. @investment is the price of the security paid at @settlement date and @redemption is the amount to be received at @maturity date.

@basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @settlement date or @maturity date is not valid, INTRATE returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, INTRATE returns #NUM! error.
* If @settlement date is after @maturity date or they are the same, INTRATE returns #NUM! error.

@EXAMPLES=

If you had a bond with a settlement date of April 15, 2000, maturity date September 30, 2000, investment of $100,000, redemption value $103,525, using the actual/actual basis, the bond discount rate is:
=INTRATE(36631, 36799, 100000, 103525, 1) which equals 0.0648 or 6.48%
@SEEALSO=RECEIVED, DATE @FUNCTION=NPER
@SYNTAX=NPER(rate,pmt,pv[,fv,type])
@DESCRIPTION=NPER calculates number of periods of an investment based on periodic constant payments and a constant interest rate.

The interest rate per period is @rate, @pmt is the payment made each period, @pv is the present value, @fv is the future value and @type is when the payments are due. If @type = 1, payments are due at the beginning of the period, if @type = 0, payments are due at the end of the period.

* If @rate <= 0, NPER returns #DIV0 error.

@EXAMPLES=
For example, if you deposit $10,000 in a savings account that earns an interest rate of 6%. To calculate how many years it will take to double your investment use NPER as follows:
=NPER(0.06, 0, -10000, 20000,0)returns 11.895661046 which indicates that you can double your money just before the end of the 12th year.
@SEEALSO=PPMT,PV,FV @FUNCTION=ODD
@SYNTAX=ODD(number)
@DESCRIPTION=ODD function returns the @number rounded up to the nearest odd integer.  Negative numbers are rounded down.

* This function is Excel compatible.
 
@EXAMPLES=
ODD(4.4) equals 5.
ODD(-4.4) equals -5.

@SEEALSO=EVEN @FUNCTION=ODDFPRICE
@SYNTAX=ODDFPRICE(settlement,maturity,issue,first_coupon,rate,yld,redemption,frequency[,basis])
@DESCRIPTION=ODDFPRICE returns the price per $100 face value of a security. The security should have an odd short or long first period.

@settlement is the settlement date of the security. @maturity is the maturity date of the security. @issue is the issue date of the security. @frequency is the number of coupon payments per year. Allowed frequencies are: 1 = annual, 2 = semi, 4 = quarterly. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, ODDFPRICE returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= @FUNCTION=ODDLPRICE
@SYNTAX=ODDLPRICE(settlement,maturity,last_interest,rate,yld,redemption,frequency[,basis])
@DESCRIPTION=ODDLPRICE calculates the price per $100 face value of a security that has an odd last coupon period.

@settlement is the settlement date of the security. @maturity is the maturity date of the security. @frequency is the number of coupon payments per year. Allowed frequencies are: 1 = annual, 2 = semi, 4 = quarterly. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, ODDLPRICE returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= @FUNCTION=OPT_2_ASSET_CORRELATION
@SYNTAX=OPT_2_ASSET_CORRELATION(call_put_flag,spot1,spot2,strike1,strike2,time,cost_of_carry1,cost_of_carry2,rate,volatility1,volatility2,rho)
@DESCRIPTION=OPT_2_ASSET_CORRELATION models the theoretical price of  options on 2 assets with correlation @rho.
The payoff for a call is max(@spot2 - @strike2,0) if @spot1 > @strike1 or 0 otherwise.
The payoff for a put is max (@strike2 - @spot2, 0) if @spot1 < @strike1 or 0 otherwise.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot1 & @spot2 are the spot prices of the underlying assets.
@strike1 & @strike2 are the strike prices at which the option is struck.
@time is the initial maturity of the option in years.
@rate is the annualized risk-free rate of interest.
@cost_of_carry1 & @cost_of_carry2 are the leakage in value of the underlying assets, for common stocks, this would be the dividend yield.
@volatility1 & @volatility2 are the annualized volatility in price of the underlying assets.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_AMER_EXCHANGE
@SYNTAX=OPT_AMER_EXCHANGE(spot1,spot2,qty1,qty2,time,rate,cost_of_carry1,cost_of_carry2,volatility1, volatility2, rho)
@DESCRIPTION=OPT_AMER_EXCHANGE models the theoretical price of an American option to exchange one asset with quantity @qty2 and spot price @spot2 for another, with quantity @qty1 and spot price @spot1.
@time is the initial maturity of the option in years.
@rate is the annualized risk-free rate of interest.
@cost_of_carry1 & @cost_of_carry2 are the leakage in value of the underlying assets, for common stocks, this would be the dividend yield.
@volatility1 & @volatility2 are the annualized volatility in price of the underlying assets.
@rho is the correlation between the two assets.

@EXAMPLES=

@SEEALSO=OPT_EURO_EXCHANGE, OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BAW_AMER
@SYNTAX=OPT_BAW_AMER(call_put_flag,spot,strike,time,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_BAW_AMER models the theoretical price of an option according to the Barone Adesie & Whaley approximation. 
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@time is the number of days to maturity of the option.
@rate is the annualized risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualized volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BINOMIAL
@SYNTAX=OPT_BINOMIAL(amer_euro_flag,call_put_flag,num_time_steps, spot, strike, time, rate, volatility, cost_of_carry)
@DESCRIPTION=OPT_ models the theoretical price of either an American or European style option using a binomial tree.
@amer_euro_flag is either 'a' or 'e' to indicate whether the option being valued is an American or European style option respectively.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@num_time_steps is the number of time steps used in the valuation, a greater number of time steps yields greater accuracy however is slower to calculate.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@time is the initial maturity of the option in years.
@rate is the annualized risk-free rate of interest.
@volatility is the annualized volatility in price of the underlying asset.
@cost_of_carry is the leakage in value of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BJER_STENS
@SYNTAX=OPT_BJER_STENS(call_put_flag,spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BJER_STENS models the theoretical price of american options according to the Bjerksund & Stensland approximation technique.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@time is the number of days to maturity of the option.
@rate is the annualized risk-free rate of interest.
@volatility is the annualized volatility in price of the underlying asset.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BS
@SYNTAX=OPT_BS(call_put_flag,spot,strike,time,rate,volatility [,cost_of_carry])
@DESCRIPTION=OPT_BS uses the Black-Scholes model to calculate the price of a European option using call_put_flag, @call_put_flag, 'c' or 'p' struck at @strike on an asset with spot price @spot.
@time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate.
@volatility is the annualized volatility, in percent, of the asset for the period through to the exercise date. 
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed in the same units as @strike and @spot.

@EXAMPLES=

@SEEALSO=OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_VEGA, OPT_BS_GAMMA @FUNCTION=OPT_BS_CARRYCOST
@SYNTAX=OPT_BS_CARRYCOST(call_put_flag,spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_CARRYCOST uses the Black-Scholes model to calculate the 'elasticity' of a European option struck at @strike on an asset with spot price @spot.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.

(The elasticity of an option is the rate of change of its price with respect to its cost of carry.)

@volatility is the annualized volatility, in percent, of the asset for the period through to the exercise date.  @time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate to the exercise date, in percent.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.

* The returned value will be expressed as the rate of change of option value, per 100% volatility.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BS_DELTA
@SYNTAX=OPT_BS_DELTA(call_put_flag,spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_DELTA uses the Black-Scholes model to calculate the 'delta' of a European option with call_put_flag, @call_put_flag, 'c' or 'p' struck at @strike on an asset with spot price @spot.
Where @time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate.
@volatility is the annualized volatility, in percent, of the asset for the period through to the exercise date. 
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed in the same units as @strike and @spot.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_VEGA, OPT_BS_GAMMA @FUNCTION=OPT_BS_GAMMA
@SYNTAX=OPT_BS_GAMMA(spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_GAMMA uses the Black-Scholes model to calculate the 'gamma' of a European option struck at @strike on an asset with spot price @spot.

(The gamma of an option is the second derivative of its price with respect to the price of the underlying asset, and is the same for calls and puts.)

@time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate to the exercise date, in percent.
@volatility is the annualized volatility, in percent, of the asset for the period through to the exercise date.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed as the rate of change of delta per unit change in @spot.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_VEGA @FUNCTION=OPT_BS_THETA
@SYNTAX=OPT_BS_THETA(call_put_flag,spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_THETA uses the Black-Scholes model to calculate the 'theta' of a European option with call_put_flag, @call_put_flag struck at @strike on an asset with spot price @spot.

(The theta of an option is the rate of change of its price with respect to time to expiry.)

@time is the time to maturity of the option expressed in years
and @rate is the risk-free interest rate to the exercise date, in percent.
@volatility is the annualized volatility, in percent, of the asset for the period through to the exercise date.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed as minus the rate of change of option value, per 365.25 days.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_VEGA, OPT_BS_GAMMA @FUNCTION=OPT_BS_VEGA
@SYNTAX=OPT_BS_VEGA(spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_VEGA uses the Black-Scholes model to calculate the 'vega' of a European option struck at @strike on an asset with spot price @spot.
(The vega of an option is the rate of change of its price with respect to volatility, and is the same for calls and puts.)
@volatility is the annualized volatility, in percent, of the asset for the period through to the exercise date.
 @time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate to the exercise date, in percent.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.

* The returned value will be expressed as the rate of change of option value, per 100% volatility.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_COMPLEX_CHOOSER
@SYNTAX=OPT_COMPLEX_CHOOSER(call_put_flag,spot,strike_call,strike_put,time,time_call,time_put,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_COMPLEX_CHOOSER models the theoretical price of complex chooser options.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike_call is the strike price at which the option is struck, applicable if exercised as a call option.
@strike_put is the strike price at which the option is struck, applicable if exercised as a put option.
@time is the time in years until the holder chooses a put or a call option. 
@time_call is the time in years to maturity of the call option if chosen.
@time_put is the time in years  to maturity of the put option if chosen.
@rate is the annualized risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualized volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_EURO_EXCHANGE
@SYNTAX=OPT_EURO_EXCHANGE(spot1,spot2,qty1,qty2,time,rate,cost_of_carry1,cost_of_carry2,volatility1,volatility2,rho)
@DESCRIPTION=OPT_EURO_EXCHANGE models the theoretical price of a European option to exchange one asset with quantity @qty2 and spot price @spot2 for another, with quantity @qty1 and spot price @spot1.
@time is the initial maturity of the option in years.
@rate is the annualized risk-free rate of interest.
@cost_of_carry1 & @cost_of_carry2 are the leakage in value of the underlying assets, for common stocks, this would be the dividend yield.
@volatility1 & @volatility2 are the annualized volatility in price of the underlying assets.
@rho is the correlation between the two assets.

@EXAMPLES=

@SEEALSO=OPT_AMER_EXCHANGE, OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_EXEC
@SYNTAX=OPT_EXEC(call_put_flag,spot,strike,time,rate,volatility,cost_of_carry,lambda)
@DESCRIPTION=OPT_EXEC models the theoretical price of executive stock options @call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
One would expect this to always be a call option.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@time is the number of days to maturity of the option.
@rate is the annualized risk-free rate of interest.
@volatility is the annualized volatility in price of the underlying asset.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@lambda is the jump rate for executives. The model assumes executives forfeit their options if they leave the company.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_EXTENDIBLE_WRITER
@SYNTAX=OPT_EXTENDIBLE_WRITER(call_put_flag,spot,strike1,strike2,time1,time2,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_EXTENDIBLE_WRITER models the theoretical price of extendible writer options. These are options that can be exercised at an initial period, @time1, or their maturity extended to @time2 if the option is out of the money at @time1.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike1 is the strike price at which the option is struck.
@strike2 is the strike price at which the option is re-struck if out of the money at @time1.
@time1 is the initial maturity of the option in years.
@time2 is the is the extended maturity in years if chosen.
@rate is the annualized risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualized volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_FIXED_STRK_LKBK
@SYNTAX=OPT_FIXED_STRK_LKBK(call_put_flag,spot,spot_min,spot_max,strike,time,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_FIXED_STRK_LKBK models the theoretical price of an option where the holder of the option may exercise on expiry at the most favourable price observed during the options life of the underlying asset.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@spot_min is the minimum spot price of the underlying asset so far observed.
@spot_max is the maximum spot price of the underlying asset so far observed.
@strike is the strike prices at which the option is struck.
@time is the initial maturity of the option in years.
@rate is the annualized risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualized volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_FLOAT_STRK_LKBK
@SYNTAX=OPT_FLOAT_STRK_LKBK(call_put_flag,spot,spot_min,spot_max,time,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_FLOAT_STRK_LKBK models the theoretical price of an option where the holder of the option may exercise on expiry at the most favourable price observed during the options life of the underlying asset.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@spot_min is the minimum spot price of the underlying asset so far observed.
@spot_max is the maximum spot price of the underlying asset so far observed.
@time is the initial maturity of the option in years.
@rate is the annualized risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualized volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_FORWARD_START
@SYNTAX=OPT_FORWARD_START(call_put_flag,spot,alpha,time1,time,rate,volatility,cost_of_carry)
@DESCRIPTION=OPT_FORWARD_START models the theoretical price of forward start options
 @call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@alpha is a fraction that set the strike price the future date @time1.
@time1 is the number of days until the option starts.
@time is the number of days to maturity of the option.
@rate is the annualized risk-free rate of interest.
@volatility is the annualized volatility in price of the underlying asset.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_FRENCH
@SYNTAX=OPT_FRENCH(call_put_flag,spot,strike,time,t2,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_FRENCH values the theoretical price of a European option adjusted for trading day volatility, struck at @strike on an asset with spot price @spot.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@volatility is the annualized volatility, in percent, of the asset for the period through to the exercise date.
 @time the number of calendar days to exercise divided by calendar days in the year.
@t2 is the number of trading days to exercise divided by trading days in the year.
@rate is the risk-free interest rate.
@cost_of_carry is the leakage in value of the underlying asset, to the exercise date, in percent.
For common stocks, this would be the dividend yield.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_GARMAN_KOHLHAGEN
@SYNTAX=OPT_GARMAN_KOHLHAGEN(call_put_flag,spot,strike,time,domestic_rate,foreign_rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_GARMAN_KOHLHAGEN values the theoretical price of a European currency option struck at @strike on an asset with spot price @spot.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@volatility is the annualized volatility, in percent, of the asset for the period through to the exercise date. 
@time the number of days to exercise.
@domestic_rate is the domestic risk-free interest rate to the exercise date.
@foreign_rate is the foreign risk-free interest rate to the exercise date, in percent.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed as the rate of change of option value, per 100% volatility.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_JUMP_DIFF
@SYNTAX=OPT_JUMP_DIFF(call_put_flag,spot,strike,time,rate,volatility,lambda,gamma)
@DESCRIPTION=OPT_JUMP_DIFF models the theoretical price of an option according to the Jump Diffusion process (Merton).
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price of the option.
@time is the time to maturity of the option expressed in years.
@rate is the annualized rate of interest.
@volatility is the annualized volatility of the underlying asset.
@lambda is expected number of 'jumps' per year.
@gamma is proportion of volatility explained by the 'jumps.'

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_ON_OPTIONS
@SYNTAX=OPT_ON_OPTIONS(type_flag,spot,strike1,strike2,time1,time2,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_ON_OPTIONS models the theoretical price of options on options.
@type_flag is 'cc' for calls on calls, 'cp' for calls on puts, and so on for 'pc', and 'pp'.
@spot is the spot price of the underlying asset.
@strike1 is the strike price at which the option being valued is struck.
@strike2 is the strike price at which the underlying option is struck.
@time1 is the time in years to maturity of the option.
@time2 is the time in years to the maturity of the underlying option.
(@time2 >= @time1).
@rate is the annualized risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset of the underlying option.for common stocks, this would be the dividend yield.
@volatility is the annualized volatility in price of the underlying asset of the underlying option.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_RGW
@SYNTAX=OPT_RGW(call_put_flag,spot,strike,t1,t2,rate,d,volatility)
@DESCRIPTION=OPT_RGW models the theoretical price of an american option according to the Roll-Geske-Whaley approximation where: 
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@t1 is the time to the dividend payout.
@t2 is the time to option expiration.
@rate is the annualized rate of interest.
@d is the amount of the dividend to be paid.
@volatility is the annualized rate of volatility of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_SPREAD_APPROX
@SYNTAX=OPT_SPREAD_APPROX(call_put_flag,fut_price1,fut_price2,strike,time, rate,volatility1,volatility2,rho)
@DESCRIPTION=OPT_SPREAD_APPROX models the theoretical price of a European option on the spread between two futures contracts.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@fut_price1 & @fut_price2 are the prices of the two futures contracts.
@strike is the strike price at which the option is struck 
@time is the initial maturity of the option in years.
@rate is the annualized risk-free rate of interest.
@volatility1 & @volatility2 are the annualized volatility in price of the underlying futures contracts.
@rho is the correlation between the two futures contracts.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_TIME_SWITCH
@SYNTAX=OPT_TIME_SWITCH(call_put_flag,spot,strike,a,time,m,dt,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_TIME_SWITCH models the theoretical price of time switch options. (Pechtl 1995)
The holder receives @a * @dt for each period dt that the asset price was greater than the strike price (for a call) or below it (for a put). 
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@a is the amount received for each time period as discussed above.
@time is the maturity of the option in years.
@m is the number of time units the option has already met the condition.
@dt is the agreed upon discrete time period (often a day) expressed as a fraction of a year.
@rate is the annualized risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=PRICE
@SYNTAX=PRICE(settle,mat,rate,yield,redemption_price,[frequency,basis])
@DESCRIPTION=PRICE returns price per $100 face value of a security. This method can only be used if the security pays periodic interest.

@frequency is the number of coupon payments per year. Allowed frequencies are: 1 = annual, 2 = semi, 4 = quarterly. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, PRICE returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= @FUNCTION=PRICEDISC
@SYNTAX=PRICEDISC(settlement,maturity,discount,redemption[,basis])
@DESCRIPTION=PRICEDISC calculates and returns the price per $100 face value of a security bond.  The security does not pay interest at maturity.

@settlement is the settlement date of the security. @maturity is the maturity date of the security.  @discount is the rate for which the security is discounted.  @redemption is the amount to be received on @maturity date.

@basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @settlement date or @maturity date is not valid, PRICEDISC returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, PRICEDISC returns #NUM! error.
* If @settlement date is after @maturity date or they are the same, PRICEDISC returns #NUM! error.

@EXAMPLES=

@SEEALSO=PRICEMAT @FUNCTION=PRICEMAT
@SYNTAX=PRICEMAT(settlement,maturity,issue,rate,yield[,basis])
@DESCRIPTION=PRICEMAT calculates and returns the price per $100 face value of a security.  The security pays interest at maturity.

@settlement is the settlement date of the security.  @maturity is the maturity date of the security.  @issue is the issue date of the security.  @rate is the discount rate of the security. @yield is the annual yield of the security. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @settlement date or @maturity date is not valid, PRICEMAT returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, PRICEMAT returns #NUM! error.
* If @settlement date is after @maturity date or they are the same, PRICEMAT returns #NUM! error.

@EXAMPLES=

@SEEALSO=PRICEDISC @FUNCTION=RANDNORMTAIL
@SYNTAX=RANDNORMTAIL(a,sigma)
@DESCRIPTION=RANDNORMTAIL returns a random variates from the upper tail of a normal distribution with standard deviation @sigma. The values returned are larger than the lower limit @a, which must be positive. The method is based on Marsaglia's famous rectangle-wedge-tail algorithm (Ann Math Stat 32, 894-899 (1961)), with this aspect explained in Knuth, v2, 3rd ed, p139, 586 (exercise 11).

The probability distribution for normal tail random variates is,

	p(x) dx = {1 over N(a;sigma)} exp (- x^2/(2 sigma^2)) dx,

for x > a where N(a;sigma) is the normalization constant, N(a;sigma) = (1/2) erfc(a / sqrt(2 sigma^2)).

@EXAMPLES=
RANDNORMTAIL(0.5,0.1).

@SEEALSO=RAND @FUNCTION=ROUNDDOWN
@SYNTAX=ROUNDDOWN(number[,digits])
@DESCRIPTION=ROUNDDOWN function rounds a given @number towards 0.

@number is the number you want rounded toward 0 and @digits is the number of digits to which you want to round that number.

* If @digits is greater than zero, @number is rounded toward 0 to the given number of digits.
* If @digits is zero or omitted, @number is rounded toward 0 to the next integer.
* If @digits is less than zero, @number is rounded toward 0 to the left of the decimal point.
* This function is Excel compatible.

@EXAMPLES=
ROUNDDOWN(5.5) equals 5.
ROUNDDOWN(-3.3) equals -3.
ROUNDDOWN(1501.15,1) equals 1501.1.
ROUNDDOWN(1501.15,-2) equals 1500.0.

@SEEALSO=ROUND,ROUNDUP @FUNCTION=ROUNDUP
@SYNTAX=ROUNDUP(number[,digits])
@DESCRIPTION=ROUNDUP function rounds a given number away from 0.

@number is the number you want rounded away from 0 and @digits is the number of digits to which you want to round that number.

* If @digits is greater than zero, @number is rounded away from 0 to the given number of digits.
* If @digits is zero or omitted, @number is rounded away from 0 to the next integer.
* If @digits is less than zero, @number is rounded away from 0 to the left of the decimal point.
* This function is Excel compatible.

@EXAMPLES=
ROUNDUP(5.5) equals 6.
ROUNDUP(-3.3) equals -4.
ROUNDUP(1501.15,1) equals 1501.2.
ROUNDUP(1501.15,-2) equals 1600.0.

@SEEALSO=ROUND,ROUNDDOWN @FUNCTION=SLN
@SYNTAX=SLN(cost,salvage_value,life)
@DESCRIPTION=SLN function will determine the straight line depreciation of an asset for a single period.

The formula is:

Depreciation expense = ( @cost - @salvage_value ) / @life

@cost is the cost of an asset when acquired (market value).
@salvage_value is the amount you get when asset is sold at the end of the asset's useful life.
@life is the anticipated life of an asset.

* If @life <= 0, SLN returns #NUM! error.

@EXAMPLES=
For example, lets suppose your company purchases a new machine for $10,000, which has a salvage value of $700 and will have a useful life of 10 years. The SLN yearly depreciation is computed as follows:
=SLN(10000, 700, 10)
This will return the yearly depreciation figure of $930.
@SEEALSO=SYD @FUNCTION=STANDARDIZE
@SYNTAX=STANDARDIZE(x,mean,stddev)
@DESCRIPTION=STANDARDIZE function returns a normalized value. @x is the number to be normalized, @mean is the mean of the distribution, @stddev is the standard deviation of the distribution.

* If @stddev is 0 STANDARDIZE returns #DIV/0! error.
* This function is Excel compatible.

@EXAMPLES=
STANDARDIZE(3,2,4) equals 0.25.

@SEEALSO=AVERAGE @FUNCTION=SYD
@SYNTAX=SYD(cost,salvage_value,life,period)
@DESCRIPTION=SYD function calculates the sum-of-years digits depreciation for an asset based on its cost, salvage value, anticipated life and a particular period. This method accelerates the rate of the depreciation, so that more depreciation expense occurs in earlier periods than in later ones. The depreciable cost is the actual cost minus the salvage value. The useful life is the number of periods (typically years) over which the asset is depreciated.

The Formula used for sum-of-years digits depreciation is:

Depreciation expense =

	 ( @cost - @salvage_value ) * (@life - @period + 1) * 2 / @life * (@life + 1).

@cost is the cost of an asset when acquired (market value).
@salvage_value is the amount you get when asset sold at the end of its useful life.
@life is the anticipated life of an asset.
@period is the period for which we need the expense.

* If @life <= 0, SYD returns #NUM! error.

@EXAMPLES=
For example say a company purchases a new computer for $5000 which has a salvage value of $200, and a useful life of five years. We would use the following to calculate the second year's depreciation using the SYD method:
=SYD(5000, 200, 5, 2) which returns 1,280.00.
@SEEALSO=SLN @FUNCTION=TBILLPRICE
@SYNTAX=TBILLPRICE(settlement,maturity,discount)
@DESCRIPTION=TBILLPRICE function returns the price per $100 value for a treasury bill where @settlement is the settlement date and @maturity is the maturity date of the bill.  @discount is the treasury bill's discount rate.

* If @settlement is after @maturity or the @maturity is set to over one year later than the @settlement, TBILLPRICE returns #NUM! error.
* If @discount is negative, TBILLPRICE returns #NUM! error.

@EXAMPLES=

@SEEALSO=TBILLEQ,TBILLYIELD @FUNCTION=TDIST
@SYNTAX=TDIST(x,dof,tails)
@DESCRIPTION=TDIST function returns the Student's t-distribution. @dof is the degree of freedom and @tails is 1 or 2 depending on whether you want one-tailed or two-tailed distribution.
@tails = 1 returns the size of the right tail.

* If @dof < 1 TDIST returns #NUM! error.
* If @tails is neither 1 or 2 TDIST returns #NUM! error.
* This function is Excel compatible for non-negative @x.

Warning: the parameterization of this function is different from what is used for, e.g., NORMSDIST.  This is a common source of mistakes, but necessary for compatibility.

@EXAMPLES=
TDIST(2,5,1) equals 0.050969739.
TDIST(-2,5,1) equals 0.949030261.
TDIST(0,5,2) equals 1.

@SEEALSO=TINV,TTEST @FUNCTION=TEXT
@SYNTAX=TEXT(value,format_text)
@DESCRIPTION=TEXT returns @value as a string with the specified format.

* This function is Excel compatible.

@EXAMPLES=
TEXT(3.223,"$0.00") equals "$3.22".
TEXT(date(1999,4,15),"mmmm, dd, yy") equals "April, 15, 99".

@SEEALSO=DOLLAR, FIXED, VALUE @FUNCTION=TINV
@SYNTAX=TINV(p,dof)
@DESCRIPTION=TINV function returns the inverse of the two-tailed Student's t-distribution.

* If @p < 0 or @p > 1 or @dof < 1 TINV returns #NUM! error.
* This function is Excel compatible.

Warning: the parameterization of this function is different from what is used for, e.g., NORMSINV.  This is a common source of mistakes, but necessary for compatibility.

@EXAMPLES=
TINV(0.4,32) equals 0.852998454.

@SEEALSO=TDIST,TTEST @FUNCTION=VALUE
@SYNTAX=VALUE(text)
@DESCRIPTION=VALUE returns numeric value of @text.

* This function is Excel compatible.

@EXAMPLES=
VALUE("$1,000") equals 1000.

@SEEALSO=DOLLAR, FIXED, TEXT @FUNCTION=YIELDDISC
@SYNTAX=YIELDDISC(settlement,maturity,pr,redemption[,basis])
@DESCRIPTION=YIELDDISC calculates the annual yield of a security that is discounted.

@settlement is the settlement date of the security.  @maturity is the maturity date of the security. @pr is the price per $100 face value of the security. @redemption is the redemption value per $100 face value. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, YIELDDISC returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= @FUNCTION=YIELDMAT
@SYNTAX=YIELDMAT(settlement,maturity,issue,rate,pr[,basis])
@DESCRIPTION=YIELDMAT calculates the annual yield of a security for which the interest is paid at maturity date.

@settlement is the settlement date of the security. @maturity is the maturity date of the security. @issue is the issue date of the security. @rate is the interest rate set to the security. @pr is the price per $100 face value of the security. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= Project-Id-Version: gnumeric 1.2
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2009-04-13 21:48+0000
PO-Revision-Date: 2008-12-22 18:20+0000
Last-Translator: David Lodge <dave@cirt.net>
Language-Team: English/GB <en_GB@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 16:17+0000
X-Generator: Launchpad (build Unknown)
 @FUNCTION=ACCRINTM
@SYNTAX=ACCRINTM(issue,maturity,rate[,par,basis])
@DESCRIPTION=ACCRINTM calculates and returns the accrued interest for a security from @issue to @maturity date.

@issue is the issue date of the security.  @maturity is the maturity date of the security.  @rate is the annual rate of the security and @par is the par value of the security. If you omit @par, ACCRINTM applies £1,000 instead.  @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @issue date or @maturity date is not valid, ACCRINTM returns #NUM! error.
* If @rate <= 0 or @par <= 0, ACCRINTM returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, ACCRINTM returns #NUM! error.
* If @issue date is after @maturity date or they are the same, ACCRINTM returns #NUM! error.

@EXAMPLES=

@SEEALSO=ACCRINT @FUNCTION=OCT2DEC
@SYNTAX=OCT2DEC(x)
@DESCRIPTION=OCT2DEC function converts an octal number in a string or number to its decimal equivalent.

* This function is Excel compatible.

@EXAMPLES=
OCT2DEC("124") equals 84.

@SEEALSO=DEC2OCT, OCT2BIN, OCT2HEX @FUNCTION=CEILING
@SYNTAX=CEILING(x,significance)
@DESCRIPTION=CEILING function rounds @x up to the nearest multiple of @significance.

* If @x or @significance is non-numeric CEILING returns #VALUE! error.
* If @x and @significance have different signs CEILING returns #NUM! error.
* This function is Excel compatible.

@EXAMPLES=
CEILING(2.43,1) equals 3.
CEILING(123.123,3) equals 126.

@SEEALSO=CEIL, FLOOR, ABS, INT, MOD @FUNCTION=OCT2DEC
@SYNTAX=OCT2DEC(x)
@DESCRIPTION=OCT2DEC function converts an octal number in a string or number to its decimal equivalent.

* This function is Excel compatible.

@EXAMPLES=
OCT2DEC("124") equals 84.

@SEEALSO=DEC2OCT, OCT2BIN, OCT2HEX @FUNCTION=DISC
@SYNTAX=DISC(settlement,maturity,par,redemption[,basis])
@DESCRIPTION=DISC calculates and returns the discount rate for a security. @settlement is the settlement date of the security.

@maturity is the maturity date of the security.  @par is the price per £100 face value of the security.  @redemption is the redemption value per £100 face value of the security.

@basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @settlement date or @maturity date is not valid, DISC returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, DISC returns #NUM! error.
* If @settlement date is after @maturity date or they are the same, DISC returns #NUM! error.

@EXAMPLES=

@SEEALSO= @FUNCTION=DOLLAR
@SYNTAX=DOLLAR(num[,decimals])
@DESCRIPTION=DOLLAR returns @num formatted as currency.

* This function is Excel compatible.

@EXAMPLES=
DOLLAR(12345) equals "£12,345.00".

@SEEALSO=FIXED, TEXT, VALUE @FUNCTION=DURATION
@SYNTAX=DURATION(settlement,maturity,coup,yield,frequency[,basis])
@DESCRIPTION=DURATION calculates the duration of a security.

@settlement is the settlement date of the security.
@maturity is the maturity date of the security.
@coup The annual coupon rate as a percentage.
@yield The annualised yield of the security as a percentage.
@frequency is the number of coupon payments per year. Allowed frequencies are: 1 = annual, 2 = semi, 4 = quarterly. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, DURATION returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO=G_DURATION,MDURATION @FUNCTION=EVEN
@SYNTAX=EVEN(number)
@DESCRIPTION=EVEN function returns the number rounded up to the nearest even integer.

* This function is Excel compatible.
 
@EXAMPLES=
EVEN(5.4) equals 6.

@SEEALSO=ODD @FUNCTION=EXPPOWDIST
@SYNTAX=EXPPOWDIST(x,a,b)
@DESCRIPTION=EXPPOWDIST returns the probability density p(x) at @x for Exponential Power distribution with scale parameter @a and exponent @b.

@EXAMPLES=
EXPPOWDIST(0.4,1,2).

@SEEALSO=RANDEXPPOW @FUNCTION=INTRATE
@SYNTAX=INTRATE(settlement,maturity,investment,redemption[,basis])
@DESCRIPTION=INTRATE calculates and returns the interest rate of a fully vested security.

@settlement is the settlement date of the security.  @maturity is the maturity date of the security. @investment is the price of the security paid at @settlement date and @redemption is the amount to be received at @maturity date.

@basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @settlement date or @maturity date is not valid, INTRATE returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, INTRATE returns #NUM! error.
* If @settlement date is after @maturity date or they are the same, INTRATE returns #NUM! error.

@EXAMPLES=

If you had a bond with a settlement date of April 15, 2000, maturity date September 30, 2000, investment of £100,000, redemption value £103,525, using the actual/actual basis, the bond discount rate is:
=INTRATE(36631, 36799, 100000, 103525, 1) which equals 0.0648 or 6.48%
@SEEALSO=RECEIVED, DATE @FUNCTION=NPER
@SYNTAX=NPER(rate,pmt,pv[,fv,type])
@DESCRIPTION=NPER calculates number of periods of an investment based on periodic constant payments and a constant interest rate.

The interest rate per period is @rate, @pmt is the payment made each period, @pv is the present value, @fv is the future value and @type is when the payments are due. If @type = 1, payments are due at the beginning of the period, if @type = 0, payments are due at the end of the period.

* If @rate <= 0, NPER returns #DIV0 error.

@EXAMPLES=
For example, if you deposit £10,000 in a savings account that earns an interest rate of 6%. To calculate home many years it will take to double your investment use NPER as follows:
=NPER(0.06, 0, -10000, 20000,0)returns 11.895661046 which indicates that you can double your money just before the end of the 12th year.
@SEEALSO=PPMT,PV,FV @FUNCTION=ODD
@SYNTAX=ODD(number)
@DESCRIPTION=ODD function returns the @number rounded up to the nearest odd integer.

* This function is Excel compatible.
 
@EXAMPLES=
ODD(4.4) equals 5.

@SEEALSO=EVEN @FUNCTION=ODDFPRICE
@SYNTAX=ODDFPRICE(settlement,maturity,issue,first_coupon,rate,yld,redemption,frequency[,basis])
@DESCRIPTION=ODDFPRICE returns the price per £100 face value of a security. The security should have an odd short or long first period.

@settlement is the settlement date of the security. @maturity is the maturity date of the security. @issue is the issue date of the security. @frequency is the number of coupon payments per year. Allowed frequencies are: 1 = annual, 2 = semi, 4 = quarterly. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, ODDFPRICE returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= @FUNCTION=ODDLPRICE
@SYNTAX=ODDLPRICE(settlement,maturity,last_interest,rate,yld,redemption,frequency[,basis])
@DESCRIPTION=ODDLPRICE calculates the price per £100 face value of a security that has an odd last coupon period.

@settlement is the settlement date of the security. @maturity is the maturity date of the security. @frequency is the number of coupon payments per year. Allowed frequencies are: 1 = annual, 2 = semi, 4 = quarterly. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, ODDLPRICE returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= @FUNCTION=OPT_2_ASSET_CORRELATION
@SYNTAX=OPT_2_ASSET_CORRELATION(call_put_flag,spot1,spot2,strike1,strike2,time,cost_of_carry1,cost_of_carry2,rate,volatility1,volatility2,rho)
@DESCRIPTION=OPT_2_ASSET_CORRELATION models the theoretical price of  options on 2 assets with correlation @rho.
The payoff for a call is max(@spot2 - @strike2,0) if @spot1 > @strike1 or 0 otherwise.
The payoff for a put is max (@strike2 - @spot2, 0) if @spot1 < @strike1 or 0 otherwise.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot1 & @spot2 are the spot prices of the underlying assets.
@strike1 & @strike2 are the strike prices at which the option is struck.
@time is the initial maturity of the option in years.
@rate is the annualised risk-free rate of interest.
@cost_of_carry1 & @cost_of_carry2 are the leakage in value of the underlying assets, for common stocks, this would be the dividend yield.
@volatility1 & @volatility2 are the annualised volatility in price of the underlying assets.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_AMER_EXCHANGE
@SYNTAX=OPT_AMER_EXCHANGE(spot1,spot2,qty1,qty2,time,rate,cost_of_carry1,cost_of_carry2,volatility1, volatility2, rho)
@DESCRIPTION=OPT_AMER_EXCHANGE models the theoretical price of an American option to exchange one asset with quantity @qty2 and spot price @spot2 for another, with quantity @qty1 and spot price @spot1.
@time is the initial maturity of the option in years.
@rate is the annualised risk-free rate of interest.
@cost_of_carry1 & @cost_of_carry2 are the leakage in value of the underlying assets, for common stocks, this would be the dividend yield.
@volatility1 & @volatility2 are the annualised volatility in price of the underlying assets.
@rho is the correlation between the two assets.

@EXAMPLES=

@SEEALSO=OPT_EURO_EXCHANGE, OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BAW_AMER
@SYNTAX=OPT_BAW_AMER(call_put_flag,spot,strike,time,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_BAW_AMER models the theoretical price of an option according to the Barone Adesie & Whaley approximation. 
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@time is the number of days to maturity of the option.
@rate is the annualised risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualised volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BINOMIAL
@SYNTAX=OPT_BINOMIAL(amer_euro_flag,call_put_flag,num_time_steps, spot, strike, time, rate, volatility, cost_of_carry)
@DESCRIPTION=OPT_ models the theoretical price of either an American or European style option using a binomial tree.
@amer_euro_flag is either 'a' or 'e' to indicate whether the option being valued is an American or European style option respectively.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@num_time_steps is the number of time steps used in the valuation, a greater number of time steps yields greater accuracy however is slower to calculate.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@time is the initial maturity of the option in years.
@rate is the annualised risk-free rate of interest.
@volatility is the annualised volatility in price of the underlying asset.
@cost_of_carry is the leakage in value of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BJER_STENS
@SYNTAX=OPT_BJER_STENS(call_put_flag,spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BJER_STENS models the theoretical price of american options according to the Bjerksund & Stensland approximation technique.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@time is the number of days to maturity of the option.
@rate is the annualised risk-free rate of interest.
@volatility is the annualised volatility in price of the underlying asset.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BS
@SYNTAX=OPT_BS(call_put_flag,spot,strike,time,rate,volatility [,cost_of_carry])
@DESCRIPTION=OPT_BS uses the Black-Scholes model to calculate the price of a European option using call_put_flag, @call_put_flag, 'c' or 'p' struck at @strike on an asset with spot price @spot.
@time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate.
@volatility is the annualised volatility, in percent, of the asset for the period through to the exercise date. 
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed in the same units as @strike and @spot.

@EXAMPLES=

@SEEALSO=OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_VEGA, OPT_BS_GAMMA @FUNCTION=OPT_BS_CARRYCOST
@SYNTAX=OPT_BS_CARRYCOST(call_put_flag,spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_CARRYCOST uses the Black-Scholes model to calculate the 'elasticity' of a European option struck at @strike on an asset with spot price @spot.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.

(The elasticity of an option is the rate of change of its price with respect to its cost of carry.)

@volatility is the annualised volatility, in percent, of the asset for the period through to the exercise date.  @time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate to the exercise date, in percent.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.

* The returned value will be expressed as the rate of change of option value, per 100% volatility.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_BS_DELTA
@SYNTAX=OPT_BS_DELTA(call_put_flag,spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_DELTA uses the Black-Scholes model to calculate the 'delta' of a European option with call_put_flag, @call_put_flag, 'c' or 'p' struck at @strike on an asset with spot price @spot.
Where @time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate.
@volatility is the annualised volatility, in percent, of the asset for the period through to the exercise date. 
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed in the same units as @strike and @spot.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_VEGA, OPT_BS_GAMMA @FUNCTION=OPT_BS_GAMMA
@SYNTAX=OPT_BS_GAMMA(spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_GAMMA uses the Black-Scholes model to calculate the 'gamma' of a European option struck at @strike on an asset with spot price @spot.

(The gamma of an option is the second derivative of its price with respect to the price of the underlying asset, and is the same for calls and puts.)

@time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate to the exercise date, in percent.
@volatility is the annualised volatility, in percent, of the asset for the period through to the exercise date.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed as the rate of change of delta per unit change in @spot.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_VEGA @FUNCTION=OPT_BS_THETA
@SYNTAX=OPT_BS_THETA(call_put_flag,spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_THETA uses the Black-Scholes model to calculate the 'theta' of a European option with call_put_flag, @call_put_flag struck at @strike on an asset with spot price @spot.

(The theta of an option is the rate of change of its price with respect to time to expiry.)

@time is the time to maturity of the option expressed in years
and @rate is the risk-free interest rate to the exercise date, in percent.
@volatility is the annualised volatility, in percent, of the asset for the period through to the exercise date.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed as minus the rate of change of option value, per 365.25 days.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_VEGA, OPT_BS_GAMMA @FUNCTION=OPT_BS_VEGA
@SYNTAX=OPT_BS_VEGA(spot,strike,time,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_BS_VEGA uses the Black-Scholes model to calculate the 'vega' of a European option struck at @strike on an asset with spot price @spot.
(The vega of an option is the rate of change of its price with respect to volatility, and is the same for calls and puts.)
@volatility is the annualised volatility, in percent, of the asset for the period through to the exercise date.
 @time is the time to maturity of the option expressed in years.
@rate is the risk-free interest rate to the exercise date, in percent.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.

* The returned value will be expressed as the rate of change of option value, per 100% volatility.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_COMPLEX_CHOOSER
@SYNTAX=OPT_COMPLEX_CHOOSER(call_put_flag,spot,strike_call,strike_put,time,time_call,time_put,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_COMPLEX_CHOOSER models the theoretical price of complex chooser options.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike_call is the strike price at which the option is struck, applicable if exercised as a call option.
@strike_put is the strike price at which the option is struck, applicable if exercised as a put option.
@time is the time in years until the holder chooses a put or a call option. 
@time_call is the time in years to maturity of the call option if chosen.
@time_put is the time in years  to maturity of the put option if chosen.
@rate is the annualised risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualised volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_EURO_EXCHANGE
@SYNTAX=OPT_EURO_EXCHANGE(spot1,spot2,qty1,qty2,time,rate,cost_of_carry1,cost_of_carry2,volatility1,volatility2,rho)
@DESCRIPTION=OPT_EURO_EXCHANGE models the theoretical price of a European option to exchange one asset with quantity @qty2 and spot price @spot2 for another, with quantity @qty1 and spot price @spot1.
@time is the initial maturity of the option in years.
@rate is the annualised risk-free rate of interest.
@cost_of_carry1 & @cost_of_carry2 are the leakage in value of the underlying assets, for common stocks, this would be the dividend yield.
@volatility1 & @volatility2 are the annualised volatility in price of the underlying assets.
@rho is the correlation between the two assets.

@EXAMPLES=

@SEEALSO=OPT_AMER_EXCHANGE, OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_EXEC
@SYNTAX=OPT_EXEC(call_put_flag,spot,strike,time,rate,volatility,cost_of_carry,lambda)
@DESCRIPTION=OPT_EXEC models the theoretical price of executive stock options @call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
One would expect this to always be a call option.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@time is the number of days to maturity of the option.
@rate is the annualised risk-free rate of interest.
@volatility is the annualised volatility in price of the underlying asset.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@lambda is the jump rate for executives. The model assumes executives forfeit their options if they leave the company.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_EXTENDIBLE_WRITER
@SYNTAX=OPT_EXTENDIBLE_WRITER(call_put_flag,spot,strike1,strike2,time1,time2,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_EXTENDIBLE_WRITER models the theoretical price of extendible writer options. These are options that can be exercised at an initial period, @time1, or their maturity extended to @time2 if the option is out of the money at @time1.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike1 is the strike price at which the option is struck.
@strike2 is the strike price at which the option is re-struck if out of the money at @time1.
@time1 is the initial maturity of the option in years.
@time2 is the is the extended maturity in years if chosen.
@rate is the annualised risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualised volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_FIXED_STRK_LKBK
@SYNTAX=OPT_FIXED_STRK_LKBK(call_put_flag,spot,spot_min,spot_max,strike,time,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_FIXED_STRK_LKBK models the theoretical price of an option where the holder of the option may exercise on expiry at the most favourable price observed during the options life of the underlying asset.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@spot_min is the minimum spot price of the underlying asset so far observed.
@spot_max is the maximum spot price of the underlying asset so far observed.
@strike is the strike prices at which the option is struck.
@time is the initial maturity of the option in years.
@rate is the annualised risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualised volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_FLOAT_STRK_LKBK
@SYNTAX=OPT_FLOAT_STRK_LKBK(call_put_flag,spot,spot_min,spot_max,time,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_FLOAT_STRK_LKBK models the theoretical price of an option where the holder of the option may exercise on expiry at the most favourable price observed during the options life of the underlying asset.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@spot_min is the minimum spot price of the underlying asset so far observed.
@spot_max is the maximum spot price of the underlying asset so far observed.
@time is the initial maturity of the option in years.
@rate is the annualised risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@volatility is the annualised volatility in price of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_FORWARD_START
@SYNTAX=OPT_FORWARD_START(call_put_flag,spot,alpha,time1,time,rate,volatility,cost_of_carry)
@DESCRIPTION=OPT_FORWARD_START models the theoretical price of forward start options
 @call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@alpha is a fraction that set the strike price the future date @time1.
@time1 is the number of days until the option starts.
@time is the number of days to maturity of the option.
@rate is the annualised risk-free rate of interest.
@volatility is the annualised volatility in price of the underlying asset.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_FRENCH
@SYNTAX=OPT_FRENCH(call_put_flag,spot,strike,time,t2,rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_FRENCH values the theoretical price of a European option adjusted for trading day volatility, struck at @strike on an asset with spot price @spot.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@volatility is the annualised volatility, in percent, of the asset for the period through to the exercise date.
 @time the number of calendar days to exercise divided by calendar days in the year.
@t2 is the number of trading days to exercise divided by trading days in the year.
@rate is the risk-free interest rate.
@cost_of_carry is the leakage in value of the underlying asset, to the exercise date, in percent.
For common stocks, this would be the dividend yield.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_GARMAN_KOHLHAGEN
@SYNTAX=OPT_GARMAN_KOHLHAGEN(call_put_flag,spot,strike,time,domestic_rate,foreign_rate,volatility[,cost_of_carry])
@DESCRIPTION=OPT_GARMAN_KOHLHAGEN values the theoretical price of a European currency option struck at @strike on an asset with spot price @spot.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@volatility is the annualised volatility, in percent, of the asset for the period through to the exercise date. 
@time the number of days to exercise.
@domestic_rate is the domestic risk-free interest rate to the exercise date.
@foreign_rate is the foreign risk-free interest rate to the exercise date, in percent.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
* The returned value will be expressed as the rate of change of option value, per 100% volatility.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_JUMP_DIFF
@SYNTAX=OPT_JUMP_DIFF(call_put_flag,spot,strike,time,rate,volatility,lambda,gamma)
@DESCRIPTION=OPT_JUMP_DIFF models the theoretical price of an option according to the Jump Diffusion process (Merton).
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price of the option.
@time is the time to maturity of the option expressed in years.
@rate is the annualised rate of interest.
@volatility is the annualised volatility of the underlying asset.
@lambda is expected number of 'jumps' per year.
@gamma is proportion of volatility explained by the 'jumps.'

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_ON_OPTIONS
@SYNTAX=OPT_ON_OPTIONS(type_flag,spot,strike1,strike2,time1,time2,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_ON_OPTIONS models the theoretical price of options on options.
@type_flag is 'cc' for calls on calls, 'cp' for calls on puts, and so on for 'pc', and 'pp'.
@spot is the spot price of the underlying asset.
@strike1 is the strike price at which the option being valued is struck.
@strike2 is the strike price at which the underlying option is struck.
@time1 is the time in years to maturity of the option.
@time2 is the time in years to the maturity of the underlying option.
(@time2 >= @time1).
@rate is the annualised risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset of the underlying option.for common stocks, this would be the dividend yield.
@volatility is the annualised volatility in price of the underlying asset of the underlying option.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_RGW
@SYNTAX=OPT_RGW(call_put_flag,spot,strike,t1,t2,rate,d,volatility)
@DESCRIPTION=OPT_RGW models the theoretical price of an american option according to the Roll-Geske-Whaley approximation where: 
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@t1 is the time to the dividend payout.
@t2 is the time to option expiration.
@rate is the annualised rate of interest.
@d is the amount of the dividend to be paid.
@volatility is the annualised rate of volatility of the underlying asset.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_SPREAD_APPROX
@SYNTAX=OPT_SPREAD_APPROX(call_put_flag,fut_price1,fut_price2,strike,time, rate,volatility1,volatility2,rho)
@DESCRIPTION=OPT_SPREAD_APPROX models the theoretical price of a European option on the spread between two futures contracts.
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@fut_price1 & @fut_price2 are the prices of the two futures contracts.
@strike is the strike price at which the option is struck 
@time is the initial maturity of the option in years.
@rate is the annualised risk-free rate of interest.
@volatility1 & @volatility2 are the annualised volatility in price of the underlying futures contracts.
@rho is the correlation between the two futures contracts.

@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=OPT_TIME_SWITCH
@SYNTAX=OPT_TIME_SWITCH(call_put_flag,spot,strike,a,time,m,dt,rate,cost_of_carry,volatility)
@DESCRIPTION=OPT_TIME_SWITCH models the theoretical price of time switch options. (Pechtl 1995)
The holder receives @a * @dt for each period dt that the asset price was greater than the strike price (for a call) or below it (for a put). 
@call_put_flag is 'c' or 'p' to indicate whether the option is a call or a put.
@spot is the spot price of the underlying asset.
@strike is the strike price at which the option is struck.
@a is the amount received for each time period as discussed above.
@time is the maturity of the option in years.
@m is the number of time units the option has already met the condition.
@dt is the agreed upon discrete time period (often a day) expressed as a fraction of a year.
@rate is the annualised risk-free rate of interest.
@cost_of_carry is the leakage in value of the underlying asset, for common stocks, this would be the dividend yield.
@EXAMPLES=

@SEEALSO=OPT_BS, OPT_BS_DELTA, OPT_BS_RHO, OPT_BS_THETA, OPT_BS_GAMMA @FUNCTION=PRICE
@SYNTAX=PRICE(settle,mat,rate,yield,redemption_price,[frequency,basis])
@DESCRIPTION=PRICE returns price per £100 face value of a security. This method can only be used if the security pays periodic interest.

@frequency is the number of coupon payments per year. Allowed frequencies are: 1 = annual, 2 = semi, 4 = quarterly. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, PRICE returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= @FUNCTION=PRICEDISC
@SYNTAX=PRICEDISC(settlement,maturity,discount,redemption[,basis])
@DESCRIPTION=PRICEDISC calculates and returns the price per £100 face value of a security bond.  The security does not pay interest at maturity.

@settlement is the settlement date of the security. @maturity is the maturity date of the security.  @discount is the rate for which the security is discounted.  @redemption is the amount to be received on @maturity date.

@basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @settlement date or @maturity date is not valid, PRICEDISC returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, PRICEDISC returns #NUM! error.
* If @settlement date is after @maturity date or they are the same, PRICEDISC returns #NUM! error.

@EXAMPLES=

@SEEALSO=PRICEMAT @FUNCTION=PRICEMAT
@SYNTAX=PRICEMAT(settlement,maturity,issue,rate,yield[,basis])
@DESCRIPTION=PRICEMAT calculates and returns the price per £100 face value of a security.  The security pays interest at maturity.

@settlement is the settlement date of the security.  @maturity is the maturity date of the security.  @issue is the issue date of the security.  @rate is the discount rate of the security. @yield is the annual yield of the security. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @settlement date or @maturity date is not valid, PRICEMAT returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis < 0 or @basis > 4, PRICEMAT returns #NUM! error.
* If @settlement date is after @maturity date or they are the same, PRICEMAT returns #NUM! error.

@EXAMPLES=

@SEEALSO=PRICEDISC @FUNCTION=RANDNORMTAIL
@SYNTAX=RANDNORMTAIL(a,sigma)
@DESCRIPTION=RANDNORMTAIL returns a random variates from the upper tail of a normal distribution with standard deviation @sigma. The values returned are larger than the lower limit @a, which must be positive. The method is based on Marsaglia's famous rectangle-wedge-tail algorithm (Ann Math Stat 32, 894-899 (1961)), with this aspect explained in Knuth, v2, 3rd ed, p139, 586 (exercise 11).

The probability distribution for normal tail random variates is,

	p(x) dx = {1 over N(a;sigma)} exp (- x^2/(2 sigma^2)) dx,

for x > a where N(a;sigma) is the normalisation constant, N(a;sigma) = (1/2) erfc(a / sqrt(2 sigma^2)).

@EXAMPLES=
RANDNORMTAIL(0.5,0.1).

@SEEALSO=RAND @FUNCTION=ROUNDDOWN
@SYNTAX=ROUNDDOWN(number[,digits])
@DESCRIPTION=ROUNDDOWN function rounds a given @number down. @number is the number you want rounded down and @digits is the number of digits to which you want to round that number.

* If @digits is greater than zero, @number is rounded down to the given number of digits.
* If @digits is zero or omitted, @number is rounded down to the nearest integer.
* If @digits is less than zero, @number is rounded down to the left of the decimal point.
* This function is Excel compatible.

@EXAMPLES=
ROUNDDOWN(5.5) equals 5.
ROUNDDOWN(-3.3) equals -4.
ROUNDDOWN(1501.15,1) equals 1501.1.
ROUNDDOWN(1501.15,-2) equals 1500.0.

@SEEALSO=ROUND,ROUNDUP @FUNCTION=ROUNDUP
@SYNTAX=ROUNDUP(number[,digits])
@DESCRIPTION=ROUNDUP function rounds a given number up.

@number is the number you want rounded up and @digits is the number of digits to which you want to round that number.

* If @digits is greater than zero, @number is rounded up to the given number of digits.
* If @digits is zero or omitted, @number is rounded up to the nearest integer.
* If @digits is less than zero, @number is rounded up to the left of the decimal point.
* This function is Excel compatible.

@EXAMPLES=
ROUNDUP(5.5) equals 6.
ROUNDUP(-3.3) equals -3.
ROUNDUP(1501.15,1) equals 1501.2.
ROUNDUP(1501.15,-2) equals 1600.0.

@SEEALSO=ROUND,ROUNDDOWN @FUNCTION=SLN
@SYNTAX=SLN(cost,salvage_value,life)
@DESCRIPTION=SLN function will determine the straight line depreciation of an asset for a single period.

The formula is:

Depreciation expense = ( @cost - @salvage_value ) / @life

@cost is the cost of an asset when acquired (market value).
@salvage_value is the amount you get when asset is sold at the end of the asset's useful life.
@life is the anticipated life of an asset.

* If @life <= 0, SLN returns #NUM! error.

@EXAMPLES=
For example, lets suppose your company purchases a new machine for £10,000, which has a salvage value of £700 and will have a useful life of 10 years. The SLN yearly depreciation is computed as follows:
=SLN(10000, 700, 10)
This will return the yearly depreciation figure of £930.
@SEEALSO=SYD @FUNCTION=STANDARDIZE
@SYNTAX=STANDARDIZE(x,mean,stddev)
@DESCRIPTION=STANDARDIZE function returns a normalised value. @x is the number to be normalised, @mean is the mean of the distribution, @stddev is the standard deviation of the distribution.

* If @stddev is 0 STANDARDIZE returns #DIV/0! error.
* This function is Excel compatible.

@EXAMPLES=
STANDARDIZE(3,2,4) equals 0.25.

@SEEALSO=AVERAGE @FUNCTION=SYD
@SYNTAX=SYD(cost,salvage_value,life,period)
@DESCRIPTION=SYD function calculates the sum-of-years digits depreciation for an asset based on its cost, salvage value, anticipated life and a particular period. This method accelerates the rate of the depreciation, so that more depreciation expense occurs in earlier periods than in later ones. The depreciable cost is the actual cost minus the salvage value. The useful life is the number of periods (typically years) over which the asset is depreciated.

The Formula used for sum-of-years digits depreciation is:

Depreciation expense =

	 ( @cost - @salvage_value ) * (@life - @period + 1) * 2 / @life * (@life + 1).

@cost is the cost of an asset when acquired (market value).
@salvage_value is the amount you get when asset sold at the end of its useful life.
@life is the anticipated life of an asset.
@period is the period for which we need the expense.

* If @life <= 0, SYD returns #NUM! error.

@EXAMPLES=
For example say a company purchases a new computer for £5000 which has a salvage value of £200, and a useful life of five years. We would use the following to calculate the second year's depreciation using the SYD method:
=SYD(5000, 200, 5, 2) which returns 1,280.00.
@SEEALSO=SLN @FUNCTION=TBILLPRICE
@SYNTAX=TBILLPRICE(settlement,maturity,discount)
@DESCRIPTION=TBILLPRICE function returns the price per £100 value for a treasury bill where @settlement is the settlement date and @maturity is the maturity date of the bill.  @discount is the treasury bill's discount rate.

* If @settlement is after @maturity or the @maturity is set to over one year later than the @settlement, TBILLPRICE returns #NUM! error.
* If @discount is negative, TBILLPRICE returns #NUM! error.

@EXAMPLES=

@SEEALSO=TBILLEQ,TBILLYIELD @FUNCTION=TDIST
@SYNTAX=TDIST(x,dof,tails)
@DESCRIPTION=TDIST function returns the Student's t-distribution. @dof is the degree of freedom and @tails is 1 or 2 depending on whether you want one-tailed or two-tailed distribution.
@tails = 1 returns the size of the right tail.

* If @dof < 1 TDIST returns #NUM! error.
* If @tails is neither 1 or 2 TDIST returns #NUM! error.
* This function is Excel compatible for non-negative @x.

Warning: the parameterisation of this function is different from what is used for, e.g., NORMSDIST.  This is a common source of mistakes, but necessary for compatibility.

@EXAMPLES=
TDIST(2,5,1) equals 0.050969739.
TDIST(-2,5,1) equals 0.949030261.
TDIST(0,5,2) equals 1.

@SEEALSO=TINV,TTEST @FUNCTION=TEXT
@SYNTAX=TEXT(value,format_text)
@DESCRIPTION=TEXT returns @value as a string with the specified format.

* This function is Excel compatible.

@EXAMPLES=
TEXT(3.223,"£0.00") equals "£3.22".
TEXT(date(1999,4,15),"mmmm, dd, yy") equals "April, 15, 99".

@SEEALSO=DOLLAR, FIXED, VALUE @FUNCTION=TINV
@SYNTAX=TINV(p,dof)
@DESCRIPTION=TINV function returns the inverse of the two-tailed Student's t-distribution.

* If @p < 0 or @p > 1 or @dof < 1 TINV returns #NUM! error.
* This function is Excel compatible.

Warning: the parameterisation of this function is different from what is used for, e.g., NORMSINV.  This is a common source of mistakes, but necessary for compatibility.

@EXAMPLES=
TINV(0.4,32) equals 0.852998454.

@SEEALSO=TDIST,TTEST @FUNCTION=VALUE
@SYNTAX=VALUE(text)
@DESCRIPTION=VALUE returns numeric value of @text.

* This function is Excel compatible.

@EXAMPLES=
VALUE("£1,000") equals 1000.

@SEEALSO=DOLLAR, FIXED, TEXT @FUNCTION=YIELDDISC
@SYNTAX=YIELDDISC(settlement,maturity,pr,redemption[,basis])
@DESCRIPTION=YIELDDISC calculates the annual yield of a security that is discounted.

@settlement is the settlement date of the security.  @maturity is the maturity date of the security. @pr is the price per £100 face value of the security. @redemption is the redemption value per £100 face value. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @frequency is other than 1, 2, or 4, YIELDDISC returns #NUM! error.
* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= @FUNCTION=YIELDMAT
@SYNTAX=YIELDMAT(settlement,maturity,issue,rate,pr[,basis])
@DESCRIPTION=YIELDMAT calculates the annual yield of a security for which the interest is paid at maturity date.

@settlement is the settlement date of the security. @maturity is the maturity date of the security. @issue is the issue date of the security. @rate is the interest rate set to the security. @pr is the price per £100 face value of the security. @basis is the type of day counting system you want to use:

  0  US 30/360
  1  actual days/actual days
  2  actual days/360
  3  actual days/365
  4  European 30/360

* If @basis is omitted, US 30/360 is applied.
* If @basis is not in between 0 and 4, #NUM! error is returned.

@EXAMPLES=

@SEEALSO= 