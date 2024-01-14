html_str = '''
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap');
        :root {
            --nicegui-default-padding: 0;
            --nicegui-default-gap: 0;
        }
        body {
            --q-primary: #0FA47F!important;
            background: #F9F9F9;
            # color: #fff;
            font-family: 'Inter', sans-serif!important;
        }
        img {
            background-color: #fff;
        }
        #c6 {
            margin-left: auto;
            margin-right: auto;
            width: 100%; 
            font-family: 'Inter', sans-serif; /* Stylish font */
            padding: 10px;
            border-radius: 5px;
        }
        #c4, .custom-footer {
            margin-left: auto;
            margin-right: auto;
            width: 60%; 
            height: auto;
        }
        .chat-area {
            margin-left: auto !important;
            margin-right: auto !important;
            height: calc(100vh - 175px) !important; 
            background-color: #F9F9F9 !important; 
            border-radius: 8px !important; 
        }
        .custom-footer {
            position: fixed;
            left: 5px;
            bottom: 0;
            padding: 10px;

        }
        .q-message {
            # box-shadow: 0px 2px 5px #202123 !important;
        }
        .q-message-sent {
            background: var(--q-primary) !important;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .q-message-received {
            background: #FFFFFF !important;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .q-message a {
            color: blue; /* Set the color of the link text to blue */
            text-decoration: underline; /* Underline the link text */
                }
        .q-message-container {
            align-items: start!important; 
            color: #1D2129;
        }

        .q-message-name {
              font-size: 15px;
              font-weight: bold;
        }
        .q-message-name--sent {
            color: #fff; 
        }
        
        .q-message-text, .q-message-text--received {
            font-family: 'Roboto', sans-serif; 
            background-color: transparent; 
            border: none; 
            color: #1D2129; 
            word-wrap: break-word; 
        }
        .q-message-text:last-child::before {
            display: none;
        }
        .q-message-text-content {
            font-size: 1rem;
            line-height: 1.5rem;
            word-spacing: 0px;
            letter-spacing: 0px;
        }
        .q-message-text-content--sent {
            color: #fff;
        }
        .q-message-text--received {
            overflow: hidden; 
            white-space: normal; 
            letter-spacing: .15em; 
            color: #1D2129;
        }
        pre {
            background-color: #f8f8f8;
            border: 1px solid #ddd;
            border-left: 3px solid #f36d33;
            color: #666;
            page-break-inside: avoid;
            font-family: monospace;
            font-size: 15px;
            line-height: 1.6;
            max-width: 100%;
            overflow: auto;
            display: block;
            padding: 1em;
            margin: 0.5em 0;
            word-wrap: break-word;
        }

        code {
            font-family: monospace;
            line-height: 1.6;
        }
        .message-left {
            display: flex;
            align-items: center;
            justify-content: start;
        }

        .message-right {
            display: flex;
            align-items: center;
            justify-content: end;
        }

        .message-box {
            padding: 10px;
            border-radius: 10px;
            margin: 5px;
            background-color: lightgray;
        }
        .q-footer {
            background: #fff;
            border-radius: 5px;
            border: 1px solid #0FA47F;

        }
        .bg-primary {
            # background: #0FA47F!important;
        }
        .dialog-wrapper > div > div.nicegui-card {
            width: 70vw;
            height: 70vh;
            padding: 20px;
            color: #000;
        }
        .dialog-card {padding: 20px; gap: 20px;}
        .dialog-form-container > .nicegui-card {padding: 20px; gap: 5px;}
        .nicegui-column, .q-field, .q-card {
            width: 100%;
        }
        </style>
    '''