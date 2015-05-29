��          4      L       `   ]  a   '   �  �  �  ^  �  '   �                    @FUNCTION=NPER
@SYNTAX=NPER(rate,pmt,pv[,fv,type])
@DESCRIPTION=NPER calculates number of periods of an investment based on periodic constant payments and a constant interest rate.

The interest rate per period is @rate, @pmt is the payment made each period, @pv is the present value, @fv is the future value and @type is when the payments are due. If @type = 1, payments are due at the beginning of the period, if @type = 0, payments are due at the end of the period.

* If @rate <= 0, NPER returns #DIV0 error.

@EXAMPLES=
For example, if you deposit $10,000 in a savings account that earns an interest rate of 6%. To calculate how many years it will take to double your investment use NPER as follows:
=NPER(0.06, 0, -10000, 20000,0)returns 11.895661046 which indicates that you can double your money just before the end of the 12th year.
@SEEALSO=PPMT,PV,FV location:the center of the distribution Project-Id-Version: gnumeric-functions
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2009-04-13 21:48+0000
PO-Revision-Date: 2009-02-17 01:50+0000
Last-Translator: Adam Weinberger <adamw@gnome.org>
Language-Team: Canadian English <adamw@gnome.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Launchpad-Export-Date: 2009-04-14 16:17+0000
X-Generator: Launchpad (build Unknown)
 @FUNCTION=NPER
@SYNTAX=NPER(rate,pmt,pv[,fv,type])
@DESCRIPTION=NPER calculates number of periods of an investment based on periodic constant payments and a constant interest rate.

The interest rate per period is @rate, @pmt is the payment made each period, @pv is the present value, @fv is the future value and @type is when the payments are due. If @type = 1, payments are due at the beginning of the period, if @type = 0, payments are due at the end of the period.

* If @rate <= 0, NPER returns #DIV0 error.

@EXAMPLES=
For example, if you deposit $10,000 in a savings account that earns an interest rate of 6%. To calculate how many years it will take to double your investment use NPER as follows:
=NPER(0.06, 0, -10000, 20000,0) returns 11.895661046 which indicates that you can double your money just before the end of the 12th year.
@SEEALSO=PPMT,PV,FV location:the centre of the distribution 