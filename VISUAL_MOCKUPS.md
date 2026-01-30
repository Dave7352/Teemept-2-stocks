# Stock Record Keeping Application - Visual Mockups

This document shows what the application looks like during use.

## Main Window

```
╔════════════════════════════════════════════════════════════════════════════════╗
║  Stock Record Keeping                                                    [_][□][X]
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                 ║
║  Stock Portfolio                          Sort by: [Total Value ▼]  [Refresh Prices]
║                                                                                 ║
║  ╔═══════════════════════════════════════════════════════════════════════════╗ ║
║  ║Ticker│Stock Name            │Shares│Price Paid│Current│Total Value│% Change│ ║
║  ╟───────────────────────────────────────────────────────────────────────────╢ ║
║  ║      │                      │      │          │       │           │        │ ║
║  ║NVDA  │Nvidia Corporation    │   3  │  $450.00 │$520.00│  $1,560.00│ +15.56%│ ║ ← Green background
║  ║AAPL  │Apple Inc.            │  10  │  $150.00 │$175.50│  $1,755.00│ +17.00%│ ║ ← Green background
║  ║AMZN  │Amazon.com Inc.       │   7  │  $145.00 │$155.75│  $1,090.25│  +7.41%│ ║ ← Green background
║  ║TSLA  │Tesla Inc.            │   8  │  $250.00 │$235.00│  $1,880.00│  -6.00%│ ║ ← Red background
║  ║GME   │GameStop Corp.        │  20  │   $45.00 │ $32.00│    $640.00│ -28.89%│ ║ ← Amber background
║  ║GE    │General Electric      │  15  │   $95.00 │ $85.00│  $1,275.00│ -10.53%│ ║ ← Orange background
║  ║ZM    │Zoom Video Comm.      │  25  │  $120.00 │ $72.00│  $1,800.00│ -40.00%│ ║ ← Gray background
║  ║      │                      │      │          │       │           │        │ ║
║  ║      │                      │      │          │       │           │        ║ ║
║  ╚═══════════════════════════════════════════════════════════════════════════╝ ║
║     ║Status        │Last Reviewed ║  ← continued columns                        ║
║     ╟──────────────┼──────────────╢                                             ║
║     ║              │              ║                                             ║
║     ║INCREASE      │Today         ║                                             ║
║     ║INCREASE      │Today         ║                                             ║
║     ║INCREASE      │Today         ║                                             ║
║     ║HOLD (Red)    │Today         ║                                             ║
║     ║INVESTIGATION │Today         ║                                             ║
║     ║DECREASE      │Today         ║                                             ║
║     ║SOLD          │Today         ║                                             ║
║                                                                                 ║
║  [Add Stock] [Edit Stock] [Delete Stock] [Mark Reviewed] [View Details] [Check Alerts]
║                                                                                 ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

## Add/Edit Stock Dialog

```
╔══════════════════════════════════════════════════════╗
║  Add Stock                                    [_][□][X]
╠══════════════════════════════════════════════════════╣
║                                                       ║
║  Stock Name:     [Apple Inc.                      ]  ║
║                                                       ║
║  Ticker:         [AAPL              ] [Fetch Info]   ║
║                                                       ║
║  Price Paid ($): [150.00                          ]  ║
║                                                       ║
║  Shares:         [10                              ]  ║
║                                                       ║
║  Current Price:  [175.50                          ]  ║
║                                                       ║
║  Position Status:[INCREASE                      ▼]  ║
║                   (INCREASE, HOLD (Green), etc.)     ║
║                                                       ║
║  Earnings Date:  [2026-02-28                      ]  ║
║                  (YYYY-MM-DD)                        ║
║                                                       ║
║  Notes:          ┌────────────────────────────────┐  ║
║                  │Tech giant with solid           │  ║
║                  │fundamentals. Recent product    │  ║
║                  │launches performing well.       │  ║
║                  │                                │  ║
║                  └────────────────────────────────┘  ║
║                                                       ║
║  Image:          No image            [Select Image]  ║
║                                                       ║
║                                                       ║
║                     [Save]  [Cancel]                 ║
║                                                       ║
╚══════════════════════════════════════════════════════╝
```

## View Details Window

```
╔══════════════════════════════════════════════════════════════╗
║  Details: Apple Inc.                              [_][□][X]  ║
╠══════════════════════════════════════════════════════════════╣
║  ┌────────────────────────────────────────────────────────┐  ║
║  │                                                        │  ║
║  │  Stock Name:        Apple Inc.                        │  ║
║  │  Ticker:            AAPL                              │  ║
║  │  Shares:            10                                │  ║
║  │  Price Paid:        $150.00                           │  ║
║  │  Current Price:     $175.50                           │  ║
║  │  Total Paid:        $1,500.00                         │  ║
║  │  Total Value:       $1,755.00                         │  ║
║  │  Gain/Loss:         +$255.00 (+17.00%)               │  ║
║  │  Position Status:   INCREASE                          │  ║
║  │  Earnings Date:     2026-02-28                        │  ║
║  │  Last Reviewed:     2026-01-30T20:08:45               │  ║
║  │  Created:           2026-01-30T20:08:45               │  ║
║  │  Modified:          2026-01-30T20:08:45               │  ║
║  │                                                        │  ║
║  │  Notes:                                               │  ║
║  │  Tech giant with solid fundamentals. Recent product   │  ║
║  │  launches performing well. Strong services growth.    │  ║
║  │  iPhone demand stable. AI initiatives promising.      │  ║
║  │                                                        │  ║
║  │  Image:                                               │  ║
║  │  ┌──────────────────────────────────────────────┐     │  ║
║  │  │                                              │     │  ║
║  │  │         [Chart or screenshot displayed]      │     │  ║
║  │  │                                              │     │  ║
║  │  └──────────────────────────────────────────────┘     │  ║
║  │                                                        │  ║
║  └────────────────────────────────────────────────────────┘  ║
║                        [Close]                               ║
╚══════════════════════════════════════════════════════════════╝
```

## Alerts Dialog

```
╔═════════════════════════════════════════════════╗
║  Alerts                                  [_][X] ║
╠═════════════════════════════════════════════════╣
║                                                  ║
║  Alerts:                                        ║
║                                                  ║
║  • GME (GameStop Corp.) - Not reviewed for      ║
║    45 days                                      ║
║                                                  ║
║  • NVDA - Earnings in 3 days (2026-02-10)      ║
║                                                  ║
║  • AAPL - Earnings in 11 days (2026-02-28)     ║
║                                                  ║
║  • GME - Investigation Required                 ║
║                                                  ║
║                                                  ║
║                     [OK]                        ║
║                                                  ║
╚═════════════════════════════════════════════════╝
```

## Price Refresh Progress

```
╔══════════════════════════════════════════╗
║  Refreshing Prices                [_][X] ║
╠══════════════════════════════════════════╣
║                                           ║
║  Fetching current prices...              ║
║                                           ║
║  [████████████████░░░░░░░░] 70%          ║
║                                           ║
╚══════════════════════════════════════════╝
```

## Complete Dialog

```
╔═══════════════════════════════════════════════════╗
║  Complete                                  [_][X] ║
╠═══════════════════════════════════════════════════╣
║                                                    ║
║  Updated 9 out of 10 stocks.                     ║
║                                                    ║
║                                                    ║
║                      [OK]                         ║
║                                                    ║
╚═══════════════════════════════════════════════════╝
```

## Color Legend

### Status Colors in Main List

```
┌─────────────────────────┬──────────────────────────┐
│ INCREASE                │ Bright Green (#00C853)   │ ← Best performers
├─────────────────────────┼──────────────────────────┤
│ HOLD (Green)            │ Light Green (#4CAF50)    │ ← Performing well
├─────────────────────────┼──────────────────────────┤
│ HOLD (Red)              │ Red (#FF5252)            │ ← Needs monitoring
├─────────────────────────┼──────────────────────────┤
│ INVESTIGATION REQUIRED  │ Amber (#FFC107)          │ ← Action needed
├─────────────────────────┼──────────────────────────┤
│ DECREASE                │ Orange (#FF6D00)         │ ← Consider reducing
├─────────────────────────┼──────────────────────────┤
│ SOLD                    │ Gray (#9E9E9E)           │ ← Historical
└─────────────────────────┴──────────────────────────┘
```

## Sample Data Display

```
Portfolio Summary (with demo data):

Total Stocks:        10
Total Value:         $15,087.50
Total Invested:      $15,870.00
Total Gain/Loss:     -$782.50 (-4.93%)

By Status:
  INCREASE:     3 stocks    $4,405.25    (+13.31%)
  HOLD (Green): 3 stocks    $5,087.25    (+8.75%)
  HOLD (Red):   1 stock     $1,880.00    (-6.00%)
  INVESTIGATION:1 stock     $640.00      (-28.89%)
  DECREASE:     1 stock     $1,275.00    (-10.53%)
  SOLD:         1 stock     $1,800.00    (-40.00%)
```

## Keyboard & Mouse Interactions

```
Main Window:
  • Double-click row    → View Details
  • Single-click row    → Select stock
  • Scroll mouse wheel  → Scroll list
  • Click sort dropdown → Change sorting

Add/Edit Dialog:
  • Tab                 → Next field
  • Shift+Tab          → Previous field
  • Enter (on button)  → Submit
  • Escape             → Cancel

All Dialogs:
  • Click [X]          → Close
  • Alt+F4            → Close window
```

## Workflow Examples

### Adding Your First Stock

```
1. Click [Add Stock]
   ↓
2. Enter: AAPL in Ticker field
   ↓
3. Click [Fetch Info]  (auto-fills name & price)
   ↓
4. Enter: 10 in Shares field
   ↓
5. Enter: 150.00 in Price Paid field
   ↓
6. Select: INCREASE from dropdown
   ↓
7. (Optional) Add notes
   ↓
8. Click [Save]
   ↓
9. Stock appears in main list!
```

### Weekly Portfolio Review

```
1. Click [Refresh Prices]
   (Wait for update to complete)
   ↓
2. Sort by: % Change
   (See best/worst performers)
   ↓
3. Double-click stocks to review
   (Check notes, update if needed)
   ↓
4. Click [Mark Reviewed] for each
   ↓
5. Click [Check Alerts]
   (See upcoming earnings & old reviews)
   ↓
6. Update position statuses as needed
   (Edit stocks that changed)
```

## Screen Resolution Support

```
Minimum:    1024 x 768   (all features work)
Recommended: 1280 x 720   (optimal layout)
Ideal:      1920 x 1080  (spacious view)

The window is resizable - drag corners to adjust!
```

## Summary

This application provides a **professional, intuitive interface** for managing stock portfolios with:
- ✅ Clear visual hierarchy
- ✅ Color-coded information
- ✅ Sortable, scrollable lists
- ✅ Modal dialogs for data entry
- ✅ Progress indicators
- ✅ Confirmation dialogs
- ✅ Keyboard shortcuts
- ✅ Mouse interactions

**Ready to use immediately after installation!**
