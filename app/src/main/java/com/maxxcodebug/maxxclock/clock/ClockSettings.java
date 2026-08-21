// SPDX-License-Identifier: GPL-3.0-only

package com.maxxcodebug.maxxclock.clock;

import android.graphics.Typeface;

import com.maxxcodebug.maxxclock.data.DataModel;

public class ClockSettings {
    // Main clock
    public DataModel.ClockStyle clockStyle;
    public boolean is24HourFormat;
    public boolean showSeconds;
    public boolean isTextUppercase;

    // Digital clock
    public Typeface digitalClockTypeface;
    public int digitalClockFontSize;

    // Analog clock
    public int analogClockSizePercent;

    // City list
    public boolean showHomeClock;
    public boolean isCityNoteEnabled;
    public String citySorting;
}
