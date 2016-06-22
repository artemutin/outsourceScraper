var AddressSlider = function(options) {
	this.$el = options.el && options.el.length ? options.el : false;
	this.o = options;
	this.globalCanGo = true;
	this.SLIDER_DELAY = 300;
	if (this.$el) {
		this.size = this.$el.find('.address-item').length;
		if ( this.size > 1 ) {
			this.count = 0;
			this.events();
			this.MIN_DELTA = 20;
			setTimeout(function() {
				this.goTo(0);
			}.bind(this), 100);
		}
	} else {
		throw new Error('Can\'t create AddressSlider');
	}
};

AddressSlider.prototype.events = function() {
	this.larrow = $('.j_mapArrow').addClass('show').filter('.left');
	this.rarrow = $('.j_mapArrow').addClass('show').filter('.right');
	this.eventType = mobilecheck() ? 'touchstart' : 'click';

	this.rarrow.off(this.eventType + '.nextaddress').on(this.eventType + '.nextaddress', function() {
		if ($(this).hasClass('loader')) { return false; }
		this.move('next');
	}.bind(this));
	this.larrow.off(this.eventType + '.prevaddress').on(this.eventType + '.prevaddress', function() {
		this.move('prev');
	}.bind(this));

	var startX;
	$('.map-address').off('touchstart.touchslider').on('touchstart.touchslider', function(e) {
		e.preventDefault();
		startX = e.originalEvent.changedTouches[0].pageX;
	}.bind(this));
	$('.map-address').off('touchend.touchslider').on('touchend.touchslider', function(e) {
		if (startX) {
			var delta = startX - e.originalEvent.changedTouches[0].pageX;
			if (!window.slider && this.rarrow.hasClass('loader')) { return false; }
			if (delta > this.MIN_DELTA) {
				this.move('next');
			} else if (delta < -this.MIN_DELTA) {
				this.move('prev');
			} else {
				var target = e.target || e.srcElement;
				if ( $(target).is('a') ) {
					var href = $(target).attr('href');
					window.location = href;
				}
			}
		}
	}.bind(this));
};

AddressSlider.prototype.move = function(dir) {
	if (this.globalCanGo && !this.loading) {
		this.globalCanGo = false;
		this.slideDelay = setTimeout(function() {
			this.globalCanGo = true;
		}.bind(this), this.SLIDER_DELAY);
		var count = this.count;
		if (!window.slider) { return false; }
		switch (dir) {
			case 'next':
				if (this.count < this.size-1 && this.canGoNext) {
					this.count++;
					this.goTo(this.count, count);
				}
				break;
			case 'prev':
				if (this.count > 0 && this.canGoPrev) {
					this.count--;
					this.goTo(this.count, count);
				}
				break;
		}
	}
};

AddressSlider.prototype.goTo = function(id, prev) {
	var el = this.getElById(id);
	if (!el.length) {
		return false;
	}
	var pos = el.position().left;
	this.rarrow.removeClass('disabled');

	this.getElById(prev).removeClass('_current');
	el.addClass('_current');

	if ( pos >= 0 ) {
		this.$el.css({
			'left': -pos
		});
	}
	var visibleWidth = 0;
	var screenWidth = this.$el.outerWidth() - this.larrow.outerWidth();
	this.$el.find('.address-item').each(function() {
		visibleWidth += $(this).outerWidth(true);
	});
	visibleWidth = visibleWidth - pos;

	if ( visibleWidth < screenWidth || this.count === this.size-1 ) {
		this.rarrow.addClass('disabled');
		this.canGoNext = false;
		this.onSlidesEnd();
	} else {
		this.rarrow.removeClass('disabled');
		this.canGoNext = true;
	}

	if ( this.count === 0 ) {
		this.larrow.addClass('disabled');
		this.canGoPrev = false;
	} else {
		this.larrow.removeClass('disabled');
		this.canGoPrev = true;
	}

	if ( !this.canGoNext && !this.canGoPrev ) {
		this.destroy();
	}
};

AddressSlider.prototype.onSlidesEnd = function() {
	if (this.o.onSlidesEnd) {
		this.o.onSlidesEnd.call(this, this);
	}
};

AddressSlider.prototype.append = function(count) {
	this.size = this.size+count;
	this.canGoNext = true;
	this.rarrow.removeClass('disabled');
};

AddressSlider.prototype.getElById = function(id) {
	return this.$el.find('[id="company_'+ id +'"]');
};

AddressSlider.prototype.destroy = function() {
	this.larrow.removeClass('show').off(this.eventType + '.prevaddress');
	this.rarrow.removeClass('show').off(this.eventType + '.nextaddress');

	this.$el.off('touchstart.touchslider')
			.off('touchend.touchslider')
			.css({'left': 0});
};

AddressSlider.prototype.loader = function(toggle) {
	if (toggle === 'show') {
		this.rarrow.addClass('loader');
		this.loading = true;
	} else if (toggle === 'hide') {
		this.rarrow.removeClass('loader');
		this.loading = false;
	}
};

// полифил BIND
if (!Function.prototype.bind) {
	Function.prototype.bind = function(oThis) {
		if (typeof this !== 'function') {
			// closest thing possible to the ECMAScript 5
			// internal IsCallable function
			throw new TypeError('Function.prototype.bind - what is trying to be bound is not callable');
		}

		var aArgs   = Array.prototype.slice.call(arguments, 1),
				fToBind = this,
				fNOP    = function() {},
				fBound  = function() {
					return fToBind.apply(this instanceof fNOP && oThis
								 ? this
								 : oThis,
								 aArgs.concat(Array.prototype.slice.call(arguments)));
				};

		fNOP.prototype = this.prototype;
		fBound.prototype = new fNOP();

		return fBound;
	};
}
