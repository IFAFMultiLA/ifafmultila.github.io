.. _codebook_prepared_data:

Codebook for MultiLA prepared tracking data
===========================================

The prepared data will be stored under

.. code-block::

    data/prepared/<application_session_id>_tracking_data.rds

in the TrackingDataScripts project. It contains a dataframe of tracked events with the following variables:

-   ``user_app_sess_code``: user application session code (session code for an individual anonymous or registered user interacting with a specific application session) -- factor
-   ``user_app_sess_user_id``: user ID for registered users; no further data on individual users is provided in this dataset -- integer for registered users or NA for anonymous users
-   ``track_sess_id``: tracking session ID (ID indicating a continuous interaction of a user with the application session on a single device) -- integer
-   ``track_sess_start``: start of the tracking session (first visit of a user on this device for this application session) -- POSIXct time
-   ``track_sess_end``: end of the tracking session (user closes the browser window of logs out) -- POSIXct time
-   ``user_agent``: "user agent"" string from the browser -- character string
-   ``client_ip``: client IP address (if it could be determined)
-   ``form_factor``: factor; ``"desktop"``, ``"tablet"`` or ``"phone"``
-   ``initial_win_width``: initial client browser window width; numeric
-   ``initial_win_height``: initial client browser window height; numeric
-   ``initial_contentview_width``: initial content view width; numeric
-   ``initial_contentview_height``: initial content view height; numeric
-   ``initial_contentscroll_width``: initial content scroll area width; numeric
-   ``initial_contentscroll_height``: initial content scroll area height; numeric
-   ``event_time``: time the event took place; POSIXct time with millisecond accuracy
-   ``type``: event type; factor; one of the following:

    - ``chapter``: change to another chapter
    - ``click``: mouse click or touch at X = ``coord1``, Y = ``coord2``
    - ``contentscroll``: scroll within the main content panel by ``coord1`` pixels in horizontal direction (usually 0)
      and ``coord2`` pixels in vertical direction
    - ``ex_result``: code exercise result after evaluation with details in ``value``
    - ``ex_submit``: code exercise submission with details in ``value``
    - ``input``: key input for a text or numerical input field with details in ``value``
    - ``input_change``: changed input value for a slider with details in ``value``
    - ``mouse``: mouse movement to X = ``coord1``, Y = ``coord2``
    - ``question_submit``: quiz question submission and result with details in ``value``; multiple answers are formatted
      there as ``[answer1, answer2, ... answern]``
    - ``scroll``: scroll of the whole website (not the main content panel) by ``coord1`` pixels in horizontal direction
      (usually 0) and ``coord2`` pixels in vertical direction; this should only happen when the browser window is very
      small; in most cases ``contentscroll`` is what you need instead;
    - ``summary_shown``: dynamic summary panel is presented for the first time
    - ``summary_topic_added``: content was added to the dynamic summary panel with the content ID in ``value``
    - ``visibility_change``: visibility status in ``value``; either "hidden" when the browser window with the application is completely occluded, minimized or invisible, else "visible"

-   ``chapter_index``: content chapter index; integer
-   ``chapter_id``: content chapter ID label; factor
-   ``ex_label``: question or exercise label; factor
-   ``ex_id``: question or exercise ID; character string
-   ``ex_event``: learnr code exercise event type; character string (``"result"`` or ``"submitted"``)
-   ``ex_output``: learnr code exercise R output; character string
-   ``ex_correct``: learnr code exercise result assessment -- correct or uncorrect; logical
-   ``xpath``: XPath to HTML element related to the event (if any); character string
-   ``css``: CSS selector to HTML element related to the event (if any); character string
-   ``value``: value related to the event; see ``type``; character string
-   ``coord1``: X coordinate for spatial events like mouse moves or clicks; numeric
-   ``coord2``: Y coordinate for spatial events like mouse moves or clicks; numeric
-   ``win_width``: current client browser window width at the time when the event occurred; numeric
-   ``win_height``: current client browser window height at the time when the event occurred; numeric
-   ``contentview_width``: current content view width at the time when the event occurred; numeric
-   ``contentview_height``: current content view height at the time when the event occurred; numeric
-   ``win_scroll_x``: current client browser window scroll X position; numeric
-   ``win_scroll_y``: current client browser window scroll Y position; numeric
-   ``content_scroll_x``: current content area scroll X position; numeric
-   ``content_scroll_y``: current content area scroll Y position; numeric
