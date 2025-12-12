# Agent/Terminal Wrapper 

When working with agents (see `@knowledge/flipside_cli.md`) it may be helpful to have terminal returns 
noticed in a conversation file, here is a template for that. 


AGENT:
QUESTION: 

-- BASH THIS 
flipside agent run <AGENT HERE> --data-json '{"question": "<QUESTION HERE>"}'

-- COPY EXACTLY RAW RETURN BELOW (space/prettify appropriately):


-- PUT YOUR ANALYSIS/SUMMARIZATION OF RESULT HERE:
