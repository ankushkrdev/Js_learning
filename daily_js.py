import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- CONFIGURATION ---
SENDER_EMAIL = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.environ.get("EMAIL_ADDRESS")

# !!! CHANGE THIS TO TODAY'S DATE (YYYY, MM, DD) !!!
COURSE_START_DATE = datetime(2026, 2, 24)

# =====================================================
# THE COMPLETE 30-DAY ADVANCED JAVASCRIPT CURRICULUM
# =====================================================
CURRICULUM = [

    # ===================================================
    # PHASE 1: ENGINE INTERNALS (Day 1-5)
    # ===================================================
    {
        "day": 1,
        "phase": "Phase 1: Engine Internals",
        "title": "How the V8 Engine Works",
        "content": """
        <h3>JavaScript is NOT interpreted — it's JIT compiled</h3>
        <p>Most people think JavaScript is an interpreted language. That was true in the 90s. Modern engines like Google's <strong>V8</strong> (used in Chrome & Node.js) use <strong>Just-In-Time (JIT) Compilation</strong> — a hybrid approach.</p>

        <h4>The Pipeline: Source Code → Machine Code</h4>
        <ol>
            <li><strong>Parser:</strong> Reads your source code and converts it into an <strong>Abstract Syntax Tree (AST)</strong>. 
                The AST is a tree representation of your code. You can visualize any JS code's AST at <code>astexplorer.net</code>.</li>
            <li><strong>Ignition (Interpreter):</strong> Takes the AST and generates <strong>Bytecode</strong>. 
                Bytecode is a lower-level representation that can run immediately. This gives you <em>fast startup</em>.</li>
            <li><strong>TurboFan (Optimizing Compiler):</strong> While the code is running, V8 monitors which functions 
                are called frequently ("hot" functions). It sends these to TurboFan, which compiles them into highly 
                optimized <strong>machine code</strong>. This gives you <em>fast execution</em>.</li>
            <li><strong>Deoptimization:</strong> If TurboFan made assumptions that turn out to be wrong 
                (e.g., a variable changed type), it throws away the optimized code and falls back to Bytecode. 
                This is called <em>deoptimization</em> or "bailing out."</li>
        </ol>

        <h4>Why this matters to you as a developer</h4>
        <p>If you write code where a variable keeps changing types (number → string → object), 
        V8 cannot optimize it. It keeps deoptimizing. This is why <strong>consistent types</strong> lead to faster code.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// BAD: V8 cannot optimize this function</span>
<span style="color:#569cd6;">function</span> add(a, b) { <span style="color:#569cd6;">return</span> a + b; }
add(1, 2);        <span style="color:#6a9955;">// V8 assumes: integers</span>
add("hello", " ") <span style="color:#6a9955;">// DEOPTIMIZED! Now it's strings</span>
add([], {})       <span style="color:#6a9955;">// DEOPTIMIZED AGAIN!</span>

<span style="color:#6a9955;">// GOOD: Consistent types</span>
<span style="color:#569cd6;">function</span> addNums(a, b) { <span style="color:#569cd6;">return</span> a + b; }
addNums(1, 2);
addNums(3, 4);
addNums(5, 6);    <span style="color:#6a9955;">// V8 optimizes: always integers ✅</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the difference between an Interpreter and a Compiler? Why does V8 use both?</li>
            <li>What is an Abstract Syntax Tree (AST), and at what stage is it created?</li>
            <li>Why does frequently changing a variable's type slow down JavaScript execution?</li>
        </ol>
        """
    },
    {
        "day": 2,
        "phase": "Phase 1: Engine Internals",
        "title": "Execution Context & Call Stack",
        "content": """
        <h3>Every line of JavaScript runs inside an Execution Context</h3>
        <p>When the JS engine runs your code, it creates an environment called an <strong>Execution Context</strong>. 
        Think of it as a box that contains: the code being executed, the variables, and the value of <code>this</code>.</p>

        <h4>Three Types of Execution Contexts</h4>
        <ul>
            <li><strong>Global Execution Context (GEC):</strong> Created when the file first loads. Only ONE exists. 
                It creates the <code>window</code> object (browser) or <code>global</code> (Node.js) and sets <code>this</code> to it.</li>
            <li><strong>Function Execution Context (FEC):</strong> Created every time a function is <em>called</em>. 
                Each function call gets its own FEC.</li>
            <li><strong>Eval Execution Context:</strong> Created inside <code>eval()</code>. Rarely used. Avoid it.</li>
        </ul>

        <h4>Two Phases of Every Execution Context</h4>
        <table border="1" cellpadding="8" style="border-collapse: collapse; width:100%;">
            <tr style="background:#eee;"><th>Creation Phase</th><th>Execution Phase</th></tr>
            <tr>
                <td>
                    1. Create the Variable Object (VO)<br>
                    2. Functions stored entirely in memory<br>
                    3. Variables set to <code>undefined</code> (hoisting)<br>
                    4. <code>this</code> is determined<br>
                    5. Scope chain is created
                </td>
                <td>
                    1. Code is executed line by line<br>
                    2. Variables are assigned actual values<br>
                    3. Functions are called (new FEC is pushed)
                </td>
            </tr>
        </table>

        <h4>The Call Stack</h4>
        <p>The Call Stack is a <strong>LIFO (Last In, First Out)</strong> data structure. When a function is called, 
        its Execution Context is pushed onto the stack. When it returns, it is popped off.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> third()  { <span style="color:#569cd6;">return</span> "done"; }
<span style="color:#569cd6;">function</span> second() { <span style="color:#569cd6;">return</span> third(); }
<span style="color:#569cd6;">function</span> first()  { <span style="color:#569cd6;">return</span> second(); }
first();

<span style="color:#6a9955;">// Call Stack (bottom to top):
// | third()  |  ← currently running
// | second() |
// | first()  |
// | Global   |  ← always at the bottom</span>
        </pre>

        <h4>Stack Overflow</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> recurse() { recurse(); }
recurse(); <span style="color:#6a9955;">// RangeError: Maximum call stack size exceeded</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>During the Creation Phase, what value does a <code>var</code> variable hold?</li>
            <li>How many Global Execution Contexts can exist in a single JS program?</li>
            <li>Draw the call stack for this code: <code>function a() { b(); } function b() { c(); } function c() {} a();</code></li>
        </ol>
        """
    },
    {
        "day": 3,
        "phase": "Phase 1: Engine Internals",
        "title": "Memory: Stack vs Heap",
        "content": """
        <h3>Where does your data actually live?</h3>
        <p>JavaScript uses two memory structures: the <strong>Stack</strong> and the <strong>Heap</strong>. 
        Understanding this prevents one of the most common bugs: accidentally mutating shared objects.</p>

        <h4>The Stack (Primitive Values)</h4>
        <p>Primitive types: <code>Number</code>, <code>String</code>, <code>Boolean</code>, <code>null</code>, 
        <code>undefined</code>, <code>Symbol</code>, <code>BigInt</code>.</p>
        <p>These are stored <strong>directly in the Stack</strong>. They are copied <strong>by value</strong>.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">let</span> a = 10;
<span style="color:#569cd6;">let</span> b = a;    <span style="color:#6a9955;">// A COPY is made</span>
b = 20;
console.log(a); <span style="color:#6a9955;">// 10 — unchanged. They are independent.</span>
        </pre>

        <h4>The Heap (Reference Values)</h4>
        <p>Objects, Arrays, Functions, Dates — anything complex is stored in the <strong>Heap</strong>. 
        The Stack only holds a <strong>pointer (memory address)</strong> to the location in the Heap.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">let</span> obj1 = { name: "Alice" };
<span style="color:#569cd6;">let</span> obj2 = obj1; <span style="color:#6a9955;">// Copies the POINTER, not the object!</span>

obj2.name = "Bob";
console.log(obj1.name); <span style="color:#6a9955;">// "Bob" — BOTH changed!</span>

<span style="color:#6a9955;">// STACK:                    HEAP:
// obj1 → 0x001  ────────→  { name: "Bob" }
// obj2 → 0x001  ────────↗</span>
        </pre>

        <h4>How to Create True Copies</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Shallow Copy (1 level deep only)</span>
<span style="color:#569cd6;">const</span> copy1 = { ...original };
<span style="color:#569cd6;">const</span> copy2 = Object.assign({}, original);

<span style="color:#6a9955;">// Deep Copy (all nested levels)</span>
<span style="color:#569cd6;">const</span> deepCopy = structuredClone(original); <span style="color:#6a9955;">// Modern</span>
<span style="color:#569cd6;">const</span> deepCopy2 = JSON.parse(JSON.stringify(original)); <span style="color:#6a9955;">// Old way (loses functions!)</span>
        </pre>

        <h4>Why <code>[] === []</code> is <code>false</code></h4>
        <p>Each <code>[]</code> creates a NEW object at a DIFFERENT address in the Heap. 
        <code>===</code> compares the memory addresses, not the contents. Two different addresses = not equal.</p>
        """,
        "quiz": """
        <ol>
            <li>If you pass an object to a function and modify it inside, does the original change? Why?</li>
            <li>What is the difference between a shallow copy and a deep copy? When does it matter?</li>
            <li>Why does <code>JSON.parse(JSON.stringify(obj))</code> fail for objects containing functions or <code>Date</code>?</li>
        </ol>
        """
    },
    {
        "day": 4,
        "phase": "Phase 1: Engine Internals",
        "title": "Garbage Collection: Mark & Sweep",
        "content": """
        <h3>How JavaScript automatically frees memory</h3>
        <p>Unlike C/C++, you don't manually allocate or free memory. JavaScript uses <strong>automatic garbage collection</strong>. 
        The most common algorithm is <strong>Mark-and-Sweep</strong>.</p>

        <h4>The Algorithm</h4>
        <ol>
            <li><strong>Mark Phase:</strong> The GC starts from "roots" (global object, currently executing functions). 
                It traverses all references from these roots and <em>marks</em> every object it can reach as "alive."</li>
            <li><strong>Sweep Phase:</strong> It scans the entire Heap. Any object that was NOT marked is considered 
                unreachable and is <em>deleted</em> (memory freed).</li>
        </ol>

        <h4>What is "Reachable"?</h4>
        <p>A value is reachable if it can be accessed through any chain of references starting from a root.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">let</span> user = { name: "John" };  <span style="color:#6a9955;">// Object is reachable via 'user'</span>
user = <span style="color:#569cd6;">null</span>;                    <span style="color:#6a9955;">// Reference removed. Object is now UNREACHABLE.</span>
                                    <span style="color:#6a9955;">// GC will collect it. ✅</span>
        </pre>

        <h4>Circular References</h4>
        <p>Old engines used "Reference Counting" which broke on circular references. Mark-and-Sweep handles this correctly.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> createCycle() {
    <span style="color:#569cd6;">let</span> a = {};
    <span style="color:#569cd6;">let</span> b = {};
    a.ref = b;
    b.ref = a;
    <span style="color:#6a9955;">// Both reference each other (cycle).</span>
}
createCycle();
<span style="color:#6a9955;">// After function ends, neither 'a' nor 'b' is reachable from root.</span>
<span style="color:#6a9955;">// Mark-and-Sweep correctly collects BOTH. ✅</span>
        </pre>

        <h4>V8's Generational Garbage Collection</h4>
        <p>V8 splits the Heap into two areas:</p>
        <ul>
            <li><strong>Young Generation (Nursery):</strong> Newly created objects live here. GC runs here very frequently (Scavenger). 
                Most objects die young (temporary variables).</li>
            <li><strong>Old Generation:</strong> Objects that survive multiple GC cycles are "promoted" here. 
                GC runs here less frequently (Mark-Sweep-Compact).</li>
        </ul>
        """,
        "quiz": """
        <ol>
            <li>Why was "Reference Counting" replaced by "Mark-and-Sweep" in modern engines?</li>
            <li>What does it mean for an object to be "reachable"?</li>
            <li>Why does V8 split the Heap into "Young" and "Old" generations?</li>
        </ol>
        """
    },
    {
        "day": 5,
        "phase": "Phase 1: Engine Internals",
        "title": "Memory Leaks & How to Prevent Them",
        "content": """
        <h3>When garbage collection fails to clean up</h3>
        <p>A memory leak happens when your code unintentionally keeps a reference to an object, 
        preventing the GC from collecting it. The memory usage keeps growing over time.</p>

        <h4>Common Memory Leak Patterns</h4>

        <p><strong>1. Accidental Global Variables</strong></p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> leaky() {
    mistake = "I am global now!"; <span style="color:#6a9955;">// No var/let/const = global variable!</span>
}
<span style="color:#6a9955;">// Fix: Always use 'use strict' or let/const.</span>
        </pre>

        <p><strong>2. Forgotten Timers</strong></p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> data = fetchHugeData();
<span style="color:#569cd6;">const</span> timer = setInterval(() => {
    process(data); <span style="color:#6a9955;">// 'data' can NEVER be collected while timer runs</span>
}, 1000);
<span style="color:#6a9955;">// Fix: clearInterval(timer) when done.</span>
        </pre>

        <p><strong>3. Detached DOM Elements</strong></p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> button = document.getElementById('btn');
document.body.removeChild(button);
<span style="color:#6a9955;">// The DOM element is removed from the page,
// but 'button' variable STILL references it in memory!
// Fix: button = null;</span>
        </pre>

        <p><strong>4. Closures Holding Large Data</strong></p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> outer() {
    <span style="color:#569cd6;">const</span> hugeArray = <span style="color:#569cd6;">new</span> Array(1000000).fill("data");
    <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span> inner() {
        console.log(hugeArray.length); <span style="color:#6a9955;">// Closure keeps hugeArray alive!</span>
    }
}
<span style="color:#569cd6;">const</span> leak = outer();
<span style="color:#6a9955;">// hugeArray is stuck in memory as long as 'leak' exists.
// Fix: Only capture what you need, not the entire array.</span>
        </pre>

        <p><strong>5. Event Listeners Not Removed</strong></p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> setup() {
    <span style="color:#569cd6;">const</span> el = document.getElementById('btn');
    el.addEventListener('click', <span style="color:#569cd6;">function</span> handler() { <span style="color:#6a9955;">/* ... */</span> });
    <span style="color:#6a9955;">// If 'el' is removed from DOM but handler is not removed,</span>
    <span style="color:#6a9955;">// both the handler AND any variables it closes over stay in memory.</span>
}
<span style="color:#6a9955;">// Fix: el.removeEventListener('click', handler);</span>
        </pre>

        <h4>How to Detect Memory Leaks</h4>
        <p>Chrome DevTools → Performance Tab → Record → Look for increasing memory. 
        Or use the Memory Tab → Take Heap Snapshots → Compare them.</p>
        """,
        "quiz": """
        <ol>
            <li>Name 3 common causes of memory leaks in a Single Page Application (SPA).</li>
            <li>How does <code>'use strict'</code> help prevent accidental global variables?</li>
            <li>How would you use Chrome DevTools to confirm a memory leak?</li>
        </ol>
        """
    },

    # ===================================================
    # PHASE 2: SCOPE & CLOSURES (Day 6-10)
    # ===================================================
    {
        "day": 6,
        "phase": "Phase 2: Scope & Closures",
        "title": "Scope Chain & Lexical Environment",
        "content": """
        <h3>JavaScript uses Lexical (Static) Scoping</h3>
        <p><strong>Lexical Scope</strong> means scope is determined by WHERE the code is physically written, 
        not where or how it is called.</p>

        <h4>Every Execution Context Has</h4>
        <ul>
            <li>A <strong>Variable Environment</strong> — where its local variables live.</li>
            <li>A reference to its <strong>Outer Environment</strong> — the environment of the parent scope 
                (where the function was <em>defined</em>).</li>
        </ul>

        <h4>The Scope Chain</h4>
        <p>When JS needs a variable, it first looks in the current scope. If not found, it follows the chain 
        to the outer scope, then the outer-outer scope, all the way to the Global scope. If still not found: <code>ReferenceError</code>.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> global = "I'm global";

<span style="color:#569cd6;">function</span> outer() {
    <span style="color:#569cd6;">const</span> outerVar = "I'm outer";
    
    <span style="color:#569cd6;">function</span> inner() {
        <span style="color:#569cd6;">const</span> innerVar = "I'm inner";
        console.log(innerVar);  <span style="color:#6a9955;">// ✅ Found locally</span>
        console.log(outerVar);  <span style="color:#6a9955;">// ✅ Found in outer scope</span>
        console.log(global);    <span style="color:#6a9955;">// ✅ Found in global scope</span>
    }
    inner();
}
outer();
        </pre>

        <h4>Tricky Example: Lexical vs Dynamic</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> b() {
    console.log(myVar); <span style="color:#6a9955;">// Where does it look?</span>
}
<span style="color:#569cd6;">function</span> a() {
    <span style="color:#569cd6;">var</span> myVar = 2;
    b(); <span style="color:#6a9955;">// Called INSIDE 'a', but...</span>
}
<span style="color:#569cd6;">var</span> myVar = 1;
a();

<span style="color:#6a9955;">// Output: 1 (NOT 2!)
// Because 'b' is DEFINED in the global scope.
// Its outer environment is Global, not 'a'.
// Lexical scope = where WRITTEN, not where CALLED.</span>
        </pre>

        <h4>Block Scope vs Function Scope</h4>
        <p><code>var</code> is function-scoped. <code>let</code> and <code>const</code> are block-scoped 
        (they respect <code>{}</code> blocks like <code>if</code>, <code>for</code>).</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">if</span> (<span style="color:#569cd6;">true</span>) {
    <span style="color:#569cd6;">var</span> x = 10;    <span style="color:#6a9955;">// Leaks out of the block!</span>
    <span style="color:#569cd6;">let</span> y = 20;    <span style="color:#6a9955;">// Stays inside the block</span>
}
console.log(x); <span style="color:#6a9955;">// 10</span>
console.log(y); <span style="color:#6a9955;">// ReferenceError</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the difference between Lexical Scope and Dynamic Scope?</li>
            <li>In the tricky example above, why does <code>b()</code> log <code>1</code> instead of <code>2</code>?</li>
            <li>Why should you prefer <code>let/const</code> over <code>var</code> from a scoping perspective?</li>
        </ol>
        """
    },
    {
        "day": 7,
        "phase": "Phase 2: Scope & Closures",
        "title": "Hoisting & Temporal Dead Zone",
        "content": """
        <h3>Hoisting is NOT moving code to the top</h3>
        <p>It's a side effect of the <strong>Creation Phase</strong> of the Execution Context. 
        Before any code runs, the engine scans for declarations and allocates memory for them.</p>

        <h4>Function Declarations: Fully Hoisted</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
sayHi(); <span style="color:#6a9955;">// ✅ Works!</span>
<span style="color:#569cd6;">function</span> sayHi() { console.log("hi"); }
<span style="color:#6a9955;">// The ENTIRE function is stored in memory during Creation Phase.</span>
        </pre>

        <h4>Function Expressions: NOT Hoisted</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
sayHi(); <span style="color:#6a9955;">// ❌ TypeError: sayHi is not a function</span>
<span style="color:#569cd6;">var</span> sayHi = <span style="color:#569cd6;">function</span>() { console.log("hi"); };
<span style="color:#6a9955;">// 'sayHi' is hoisted as 'undefined' (it's a var).
// You're trying to call undefined().</span>
        </pre>

        <h4><code>var</code> Hoisting</h4>
        <p>The variable name is hoisted, but initialized as <code>undefined</code>.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
console.log(x); <span style="color:#6a9955;">// undefined (not ReferenceError!)</span>
<span style="color:#569cd6;">var</span> x = 5;
        </pre>

        <h4><code>let/const</code> and the Temporal Dead Zone (TDZ)</h4>
        <p><code>let</code> and <code>const</code> ARE hoisted — but they are NOT initialized. 
        They sit in the <strong>Temporal Dead Zone</strong> from the start of the block until the declaration line.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// ┌── TDZ for 'x' starts here ──┐</span>
console.log(x); <span style="color:#6a9955;">// ❌ ReferenceError    │</span>
<span style="color:#569cd6;">let</span> x = 10;     <span style="color:#6a9955;">// ← TDZ ends here ───┘</span>
console.log(x); <span style="color:#6a9955;">// 10 ✅</span>
        </pre>

        <h4>Class Hoisting</h4>
        <p>Classes are also hoisted but are in the TDZ, similar to <code>let</code>.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> obj = <span style="color:#569cd6;">new</span> MyClass(); <span style="color:#6a9955;">// ❌ ReferenceError</span>
<span style="color:#569cd6;">class</span> MyClass {}
        </pre>
        """,
        "quiz": """
        <ol>
            <li>Is <code>let</code> hoisted? If yes, why does accessing it before declaration throw an error?</li>
            <li>What is the output? <code>var a = 1; function a() {} console.log(typeof a);</code></li>
            <li>What is the Temporal Dead Zone, and which declarations are affected by it?</li>
        </ol>
        """
    },
    {
        "day": 8,
        "phase": "Phase 2: Scope & Closures",
        "title": "IIFE & The Module Pattern",
        "content": """
        <h3>IIFE: Immediately Invoked Function Expressions</h3>
        <p>An IIFE is a function that runs as soon as it is defined. It was the primary way to create private scope before ES6 modules.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
(<span style="color:#569cd6;">function</span>() {
    <span style="color:#569cd6;">var</span> secret = "hidden";
    console.log("I run immediately!");
})();
console.log(secret); <span style="color:#6a9955;">// ❌ ReferenceError — private!</span>
        </pre>

        <h4>Why wrap in parentheses?</h4>
        <p>Without them, JS sees <code>function</code> as a <em>declaration</em> (which needs a name). 
        The <code>()</code> wrapping tells the parser: "this is an <em>expression</em>, not a declaration."</p>

        <h4>The Revealing Module Pattern</h4>
        <p>Before ES6 <code>import/export</code>, this was THE way to create modules with public and private members:</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> Counter = (<span style="color:#569cd6;">function</span>() {
    <span style="color:#6a9955;">// Private variable — cannot be accessed from outside</span>
    <span style="color:#569cd6;">let</span> count = 0;
    
    <span style="color:#6a9955;">// Private function</span>
    <span style="color:#569cd6;">function</span> log() { console.log(<span style="color:#ce9178;">`Count: </span><span style="color:#569cd6;">${count}</span><span style="color:#ce9178;">`</span>); }
    
    <span style="color:#6a9955;">// Public API — only these are exposed</span>
    <span style="color:#569cd6;">return</span> {
        increment: <span style="color:#569cd6;">function</span>() { count++; log(); },
        decrement: <span style="color:#569cd6;">function</span>() { count--; log(); },
        getCount:  <span style="color:#569cd6;">function</span>() { <span style="color:#569cd6;">return</span> count; }
    };
})();

Counter.increment(); <span style="color:#6a9955;">// Count: 1</span>
Counter.increment(); <span style="color:#6a9955;">// Count: 2</span>
Counter.count;       <span style="color:#6a9955;">// undefined — it's private!</span>
        </pre>

        <h4>Modern Equivalent: ES Modules</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// counter.js</span>
<span style="color:#569cd6;">let</span> count = 0; <span style="color:#6a9955;">// Private by default in a module</span>
<span style="color:#569cd6;">export function</span> increment() { count++; }
<span style="color:#569cd6;">export function</span> getCount() { <span style="color:#569cd6;">return</span> count; }
        </pre>
        """,
        "quiz": """
        <ol>
            <li>Why can't external code access variables inside an IIFE?</li>
            <li>In the Module Pattern, what mechanism allows <code>increment()</code> to access <code>count</code> even after the IIFE has finished?</li>
            <li>What advantages do ES Modules have over the IIFE Module Pattern?</li>
        </ol>
        """
    },
    {
        "day": 9,
        "phase": "Phase 2: Scope & Closures",
        "title": "Closures Deep Dive",
        "content": """
        <h3>A closure is a function + its lexical environment</h3>
        <p>When a function is returned from another function, it "remembers" the variables from its parent scope — 
        even after the parent has finished executing. This bundled combination is a <strong>closure</strong>.</p>

        <h4>The Core Mechanism</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> createCounter() {
    <span style="color:#569cd6;">let</span> count = 0; <span style="color:#6a9955;">// This should be garbage collected... but it won't be.</span>
    
    <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span>() {
        count++;
        <span style="color:#569cd6;">return</span> count;
    };
}

<span style="color:#569cd6;">const</span> counter = createCounter();
console.log(counter()); <span style="color:#6a9955;">// 1</span>
console.log(counter()); <span style="color:#6a9955;">// 2</span>
console.log(counter()); <span style="color:#6a9955;">// 3</span>

<span style="color:#6a9955;">// createCounter() has LONG finished executing.
// But 'count' is still alive because the inner function holds a reference.
// The GC sees this reference and keeps 'count' in the Heap.</span>
        </pre>

        <h4>The Classic Loop Problem</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// ❌ BUG: Prints "3" three times</span>
<span style="color:#569cd6;">for</span> (<span style="color:#569cd6;">var</span> i = 0; i < 3; i++) {
    setTimeout(<span style="color:#569cd6;">function</span>() {
        console.log(i); <span style="color:#6a9955;">// All callbacks share the SAME 'i'</span>
    }, 1000);
}
<span style="color:#6a9955;">// By the time setTimeout fires, the loop is done and i === 3.</span>

<span style="color:#6a9955;">// ✅ FIX 1: Use 'let' (creates a new binding per iteration)</span>
<span style="color:#569cd6;">for</span> (<span style="color:#569cd6;">let</span> i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 1000); <span style="color:#6a9955;">// 0, 1, 2</span>
}

<span style="color:#6a9955;">// ✅ FIX 2: Use a closure (IIFE captures current value)</span>
<span style="color:#569cd6;">for</span> (<span style="color:#569cd6;">var</span> i = 0; i < 3; i++) {
    (<span style="color:#569cd6;">function</span>(j) {
        setTimeout(() => console.log(j), 1000);
    })(i); <span style="color:#6a9955;">// Pass 'i' as argument 'j' — creates a new scope</span>
}
        </pre>

        <h4>Closures in DevTools</h4>
        <p>You can see closures in Chrome DevTools: Set a breakpoint inside a nested function → 
        Look at the <strong>Scope</strong> panel → You'll see a section labeled <code>Closure</code> listing the captured variables.</p>
        """,
        "quiz": """
        <ol>
            <li>Why does using <code>let</code> in a for-loop fix the closure problem, but <code>var</code> does not?</li>
            <li>Are closures stored on the Stack or the Heap? Why?</li>
            <li>Write a function <code>multiplier(x)</code> that returns another function which multiplies its argument by <code>x</code>. Use a closure.</li>
        </ol>
        """
    },
    {
        "day": 10,
        "phase": "Phase 2: Scope & Closures",
        "title": "Closure Use Cases: Memoization & Data Privacy",
        "content": """
        <h3>Practical uses of closures in real code</h3>

        <h4>1. Memoization (Caching expensive computations)</h4>
        <p>A memoized function stores the results of previous calls. If called again with the same arguments, 
        it returns the cached result instantly instead of recalculating.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> memoize(fn) {
    <span style="color:#569cd6;">const</span> cache = {}; <span style="color:#6a9955;">// Closure keeps this alive</span>
    
    <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span>(...args) {
        <span style="color:#569cd6;">const</span> key = JSON.stringify(args);
        
        <span style="color:#569cd6;">if</span> (cache[key] !== <span style="color:#569cd6;">undefined</span>) {
            console.log("From cache!");
            <span style="color:#569cd6;">return</span> cache[key];
        }
        
        <span style="color:#569cd6;">const</span> result = fn(...args);
        cache[key] = result;
        <span style="color:#569cd6;">return</span> result;
    };
}

<span style="color:#569cd6;">const</span> expensiveAdd = memoize((a, b) => {
    console.log("Calculating...");
    <span style="color:#569cd6;">return</span> a + b;
});

expensiveAdd(1, 2); <span style="color:#6a9955;">// "Calculating..." → 3</span>
expensiveAdd(1, 2); <span style="color:#6a9955;">// "From cache!" → 3 (instant!)</span>
        </pre>

        <h4>2. Data Privacy (Private Variables)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> createBankAccount(initialBalance) {
    <span style="color:#569cd6;">let</span> balance = initialBalance; <span style="color:#6a9955;">// Private! Cannot be accessed directly.</span>
    
    <span style="color:#569cd6;">return</span> {
        deposit(amount) {
            <span style="color:#569cd6;">if</span> (amount > 0) balance += amount;
            <span style="color:#569cd6;">return</span> balance;
        },
        withdraw(amount) {
            <span style="color:#569cd6;">if</span> (amount > 0 && amount <= balance) balance -= amount;
            <span style="color:#569cd6;">return</span> balance;
        },
        getBalance() { <span style="color:#569cd6;">return</span> balance; }
    };
}

<span style="color:#569cd6;">const</span> account = createBankAccount(100);
account.deposit(50);     <span style="color:#6a9955;">// 150</span>
account.withdraw(30);    <span style="color:#6a9955;">// 120</span>
account.balance;         <span style="color:#6a9955;">// undefined — can't access directly!</span>
account.getBalance();    <span style="color:#6a9955;">// 120</span>
        </pre>

        <h4>3. Function Factories</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> createGreeter(greeting) {
    <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span>(name) {
        <span style="color:#569cd6;">return</span> <span style="color:#ce9178;">`</span><span style="color:#569cd6;">${greeting}</span><span style="color:#ce9178;">, </span><span style="color:#569cd6;">${name}</span><span style="color:#ce9178;">!`</span>;
    };
}
<span style="color:#569cd6;">const</span> sayHello = createGreeter("Hello");
<span style="color:#569cd6;">const</span> sayHola  = createGreeter("Hola");
sayHello("Alice"); <span style="color:#6a9955;">// "Hello, Alice!"</span>
sayHola("Bob");    <span style="color:#6a9955;">// "Hola, Bob!"</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>In the memoize function, what would happen if <code>cache</code> was declared outside of <code>memoize</code> as a global? What problem could that cause?</li>
            <li>Why is the <code>balance</code> variable in the bank account example truly private? Can you think of any way to hack into it?</li>
            <li>Implement a <code>once(fn)</code> function using closures that only allows <code>fn</code> to be called one time. Subsequent calls should return the first result.</li>
        </ol>
        """
    },

    # ===================================================
    # PHASE 3: THIS & OBJECTS (Day 11-15)
    # ===================================================
    {
        "day": 11,
        "phase": "Phase 3: this & Objects",
        "title": "The 'this' Keyword — 4 Rules",
        "content": """
        <h3><code>this</code> is determined by HOW a function is called, not where it's defined</h3>
        <p>Unlike most concepts in JS (which are lexical), <code>this</code> is <strong>dynamic</strong>. 
        It can change depending on the call site.</p>

        <h4>Rule 1: Default Binding (Standalone Call)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> show() { console.log(<span style="color:#569cd6;">this</span>); }
show(); <span style="color:#6a9955;">// window (browser) or global (Node)</span>
        <span style="color:#6a9955;">// In strict mode: undefined</span>
        </pre>

        <h4>Rule 2: Implicit Binding (Method Call)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> obj = {
    name: "JS",
    greet() { console.log(<span style="color:#569cd6;">this</span>.name); }
};
obj.greet(); <span style="color:#6a9955;">// "JS" — 'this' = the object BEFORE the dot</span>
        </pre>

        <h4>Rule 3: Explicit Binding (call / apply / bind)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> greet() { console.log(<span style="color:#569cd6;">this</span>.name); }
<span style="color:#569cd6;">const</span> person = { name: "Alice" };
greet.call(person);  <span style="color:#6a9955;">// "Alice" — 'this' is explicitly set</span>
        </pre>

        <h4>Rule 4: <code>new</code> Binding (Constructor Call)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> User(name) { <span style="color:#569cd6;">this</span>.name = name; }
<span style="color:#569cd6;">const</span> u = <span style="color:#569cd6;">new</span> User("Bob");
<span style="color:#6a9955;">// 'new' creates a brand new empty object {}</span>
<span style="color:#6a9955;">// 'this' inside User points to that new object</span>
<span style="color:#6a9955;">// The object is returned automatically</span>
        </pre>

        <h4>Priority Order (Highest to Lowest)</h4>
        <p><code>new</code> > <code>call/apply/bind</code> > <code>obj.method()</code> > <code>standalone()</code></p>

        <h4>The Implicit Binding Loss Problem</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> obj = {
    name: "JS",
    greet() { console.log(<span style="color:#569cd6;">this</span>.name); }
};
<span style="color:#569cd6;">const</span> fn = obj.greet; <span style="color:#6a9955;">// Extracting the function</span>
fn(); <span style="color:#6a9955;">// undefined! 'this' is now window, not obj.</span>
<span style="color:#6a9955;">// The dot context is LOST. It's now a standalone call (Rule 1).</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What are the 4 rules of <code>this</code> binding in order of priority?</li>
            <li>Why does extracting a method (<code>const fn = obj.method</code>) cause <code>this</code> to change?</li>
            <li>What does <code>this</code> refer to inside a function in <code>'use strict'</code> mode when called standalone?</li>
        </ol>
        """
    },
    {
        "day": 12,
        "phase": "Phase 3: this & Objects",
        "title": "call, apply, bind & Arrow Functions",
        "content": """
        <h3>Explicitly controlling <code>this</code></h3>

        <h4><code>.call(thisArg, arg1, arg2, ...)</code></h4>
        <p>Calls the function immediately with a specific <code>this</code>. Arguments passed individually.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> introduce(greeting) {
    console.log(<span style="color:#ce9178;">`</span><span style="color:#569cd6;">${greeting}</span><span style="color:#ce9178;">, I'm </span><span style="color:#569cd6;">${this.name}</span><span style="color:#ce9178;">`</span>);
}
introduce.call({ name: "Alice" }, "Hello"); <span style="color:#6a9955;">// "Hello, I'm Alice"</span>
        </pre>

        <h4><code>.apply(thisArg, [argsArray])</code></h4>
        <p>Same as <code>call</code>, but arguments are passed as an array.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
introduce.apply({ name: "Bob" }, ["Hi"]); <span style="color:#6a9955;">// "Hi, I'm Bob"</span>
<span style="color:#6a9955;">// Useful for: Math.max.apply(null, [1,2,3]) → 3</span>
        </pre>

        <h4><code>.bind(thisArg)</code></h4>
        <p>Does NOT call the function. Returns a <strong>new function</strong> with <code>this</code> permanently set.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> boundFn = introduce.bind({ name: "Charlie" });
boundFn("Hey"); <span style="color:#6a9955;">// "Hey, I'm Charlie"</span>
boundFn("Yo");  <span style="color:#6a9955;">// "Yo, I'm Charlie" — 'this' is locked forever</span>
        </pre>

        <h4>Arrow Functions: Lexical <code>this</code></h4>
        <p>Arrow functions do NOT have their own <code>this</code>. They inherit <code>this</code> from the 
        enclosing scope (lexically). <code>call/apply/bind</code> CANNOT override it.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> obj = {
    name: "JS",
    regular: <span style="color:#569cd6;">function</span>() { console.log(<span style="color:#569cd6;">this</span>.name); },
    arrow: () => { console.log(<span style="color:#569cd6;">this</span>.name); }
};
obj.regular(); <span style="color:#6a9955;">// "JS"       — 'this' = obj</span>
obj.arrow();   <span style="color:#6a9955;">// undefined  — 'this' = window (parent scope)</span>

<span style="color:#6a9955;">// WHEN TO USE ARROWS: Inside methods, for callbacks</span>
<span style="color:#569cd6;">const</span> team = {
    members: ["Alice", "Bob"],
    name: "Dev Team",
    list() {
        <span style="color:#6a9955;">// Arrow inherits 'this' from list(), which is 'team'</span>
        <span style="color:#569cd6;">this</span>.members.forEach(m => {
            console.log(<span style="color:#ce9178;">`</span><span style="color:#569cd6;">${m}</span><span style="color:#ce9178;"> belongs to </span><span style="color:#569cd6;">${this.name}</span><span style="color:#ce9178;">`</span>); <span style="color:#6a9955;">// ✅ Works!</span>
        });
    }
};
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the key difference between <code>call</code> and <code>apply</code>?</li>
            <li>Can you use <code>.bind()</code> on an arrow function to change its <code>this</code>? Why or why not?</li>
            <li>Write a <code>polyfill</code> (your own implementation) for <code>Function.prototype.bind</code>.</li>
        </ol>
        """
    },
    {
        "day": 13,
        "phase": "Phase 3: this & Objects",
        "title": "Prototypal Inheritance",
        "content": """
        <h3>JavaScript does NOT have classical inheritance. It has prototypes.</h3>
        <p>Every object in JavaScript has a hidden property called <code>[[Prototype]]</code> 
        (accessible via <code>__proto__</code> or <code>Object.getPrototypeOf()</code>). 
        This links to another object — the prototype.</p>

        <h4>How Property Lookup Works</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> animal = {
    eats: <span style="color:#569cd6;">true</span>,
    walk() { console.log("Walking"); }
};

<span style="color:#569cd6;">const</span> dog = Object.create(animal); <span style="color:#6a9955;">// dog's [[Prototype]] → animal</span>
dog.barks = <span style="color:#569cd6;">true</span>;

console.log(dog.barks); <span style="color:#6a9955;">// true — found on 'dog' itself</span>
console.log(dog.eats);  <span style="color:#6a9955;">// true — NOT on 'dog', found on prototype (animal)</span>
dog.walk();             <span style="color:#6a9955;">// "Walking" — inherited from animal</span>
        </pre>

        <h4>Constructor Functions (Pre-ES6 way)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> Person(name) {
    <span style="color:#569cd6;">this</span>.name = name;
}
Person.prototype.greet = <span style="color:#569cd6;">function</span>() {
    console.log(<span style="color:#ce9178;">`Hi, I'm </span><span style="color:#569cd6;">${this.name}</span><span style="color:#ce9178;">`</span>);
};

<span style="color:#569cd6;">const</span> alice = <span style="color:#569cd6;">new</span> Person("Alice");
alice.greet(); <span style="color:#6a9955;">// "Hi, I'm Alice"</span>

<span style="color:#6a9955;">// What 'new' does internally:
// 1. Creates empty object: {}
// 2. Sets its [[Prototype]] to Person.prototype
// 3. Calls Person() with 'this' = new object
// 4. Returns the object</span>
        </pre>

        <h4>Own vs Inherited Properties</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
alice.hasOwnProperty('name');  <span style="color:#6a9955;">// true  — defined directly on alice</span>
alice.hasOwnProperty('greet'); <span style="color:#6a9955;">// false — inherited from prototype</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the difference between <code>__proto__</code> and <code>.prototype</code>?</li>
            <li>What are the 4 things the <code>new</code> keyword does internally?</li>
            <li>Why is it better to put methods on <code>.prototype</code> instead of inside the constructor?</li>
        </ol>
        """
    },
    {
        "day": 14,
        "phase": "Phase 3: this & Objects",
        "title": "The Prototype Chain",
        "content": """
        <h3>Everything leads to <code>Object.prototype</code>, then <code>null</code></h3>
        <p>The Prototype Chain is the linked list of prototypes that JS traverses when looking up a property.</p>

        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> arr = [1, 2, 3];

<span style="color:#6a9955;">// Chain:
// arr → Array.prototype → Object.prototype → null
//
// arr.push(4)     — found on Array.prototype ✅
// arr.toString()  — found on Object.prototype ✅
// arr.fly()       — not found anywhere → undefined</span>
        </pre>

        <h4>Visualizing the Chain</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> Animal(name) { <span style="color:#569cd6;">this</span>.name = name; }
Animal.prototype.eat = <span style="color:#569cd6;">function</span>() { console.log("eating"); };

<span style="color:#569cd6;">function</span> Dog(name, breed) {
    Animal.call(<span style="color:#569cd6;">this</span>, name); <span style="color:#6a9955;">// Call parent constructor</span>
    <span style="color:#569cd6;">this</span>.breed = breed;
}
Dog.prototype = Object.create(Animal.prototype); <span style="color:#6a9955;">// Link prototypes</span>
Dog.prototype.constructor = Dog; <span style="color:#6a9955;">// Fix constructor reference</span>
Dog.prototype.bark = <span style="color:#569cd6;">function</span>() { console.log("Woof!"); };

<span style="color:#569cd6;">const</span> rex = <span style="color:#569cd6;">new</span> Dog("Rex", "Labrador");
rex.bark(); <span style="color:#6a9955;">// "Woof!"   — found on Dog.prototype</span>
rex.eat();  <span style="color:#6a9955;">// "eating"  — found on Animal.prototype</span>

<span style="color:#6a9955;">// Chain: rex → Dog.prototype → Animal.prototype → Object.prototype → null</span>
        </pre>

        <h4>ES6 Class Syntax (Sugar over Prototypes)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">class</span> Animal {
    constructor(name) { <span style="color:#569cd6;">this</span>.name = name; }
    eat() { console.log("eating"); }
}

<span style="color:#569cd6;">class</span> Dog <span style="color:#569cd6;">extends</span> Animal {
    constructor(name, breed) {
        <span style="color:#569cd6;">super</span>(name); <span style="color:#6a9955;">// Calls Animal's constructor</span>
        <span style="color:#569cd6;">this</span>.breed = breed;
    }
    bark() { console.log("Woof!"); }
}
<span style="color:#6a9955;">// Under the hood: EXACT same prototype chain as above!</span>
        </pre>

        <h4>Performance Note</h4>
        <p>Looking up deeply nested prototype chains is slower. If you access <code>obj.x</code> and <code>x</code> 
        is 5 levels up the chain, the engine must traverse all 5. V8 optimizes this with <strong>Inline Caches</strong>, 
        but awareness of chain depth matters.</p>
        """,
        "quiz": """
        <ol>
            <li>What is at the very end of every prototype chain in JavaScript?</li>
            <li>What does <code>Object.create(null)</code> create, and why might you use it?</li>
            <li>ES6 <code>class</code> syntax is often called "syntactic sugar." What does it translate to under the hood?</li>
        </ol>
        """
    },
    {
        "day": 15,
        "phase": "Phase 3: this & Objects",
        "title": "Property Descriptors & Object.defineProperty",
        "content": """
        <h3>Properties are more than just key-value pairs</h3>
        <p>Every property on an object has hidden attributes called <strong>Property Descriptors</strong>.</p>

        <h4>The Descriptor Object</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> obj = { name: "JS" };
console.log(Object.getOwnPropertyDescriptor(obj, 'name'));
<span style="color:#6a9955;">// {
//   value: "JS",
//   writable: true,      — Can the value be changed?
//   enumerable: true,    — Does it show up in for...in loops?
//   configurable: true   — Can the descriptor be modified / property deleted?
// }</span>
        </pre>

        <h4>Creating Controlled Properties</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> user = {};
Object.defineProperty(user, 'id', {
    value: 42,
    writable: <span style="color:#569cd6;">false</span>,      <span style="color:#6a9955;">// Cannot change</span>
    enumerable: <span style="color:#569cd6;">false</span>,    <span style="color:#6a9955;">// Hidden from loops</span>
    configurable: <span style="color:#569cd6;">false</span>  <span style="color:#6a9955;">// Cannot delete or reconfigure</span>
});

user.id = 100; <span style="color:#6a9955;">// Silently fails (or throws in strict mode)</span>
console.log(user.id); <span style="color:#6a9955;">// 42</span>
console.log(Object.keys(user)); <span style="color:#6a9955;">// [] — 'id' is hidden!</span>
        </pre>

        <h4>Getters and Setters</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> person = {
    firstName: "John",
    lastName: "Doe",
    
    <span style="color:#569cd6;">get</span> fullName() {
        <span style="color:#569cd6;">return</span> <span style="color:#ce9178;">`</span><span style="color:#569cd6;">${this.firstName} ${this.lastName}</span><span style="color:#ce9178;">`</span>;
    },
    <span style="color:#569cd6;">set</span> fullName(value) {
        [<span style="color:#569cd6;">this</span>.firstName, <span style="color:#569cd6;">this</span>.lastName] = value.split(" ");
    }
};

console.log(person.fullName);       <span style="color:#6a9955;">// "John Doe" (getter)</span>
person.fullName = "Jane Smith";     <span style="color:#6a9955;">// (setter)</span>
console.log(person.firstName);      <span style="color:#6a9955;">// "Jane"</span>
        </pre>

        <h4>Freezing Objects</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> config = { api: "https://...", debug: <span style="color:#569cd6;">false</span> };
Object.freeze(config);   <span style="color:#6a9955;">// Nothing can be changed, added, or deleted</span>
Object.seal(config);     <span style="color:#6a9955;">// Values can change, but no add/delete</span>
Object.preventExtensions(config); <span style="color:#6a9955;">// No new properties, but can modify/delete</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the difference between <code>Object.freeze()</code> and <code>Object.seal()</code>?</li>
            <li>Is <code>Object.freeze()</code> deep or shallow? How would you deep-freeze an object?</li>
            <li>How would you create a truly constant object where nested objects are also immutable?</li>
        </ol>
        """
    },

    # ===================================================
    # PHASE 4: ADVANCED FUNCTIONS (Day 16-20)
    # ===================================================
    {
        "day": 16,
        "phase": "Phase 4: Advanced Functions",
        "title": "Higher-Order Functions & Function Composition",
        "content": """
        <h3>Functions that operate on other functions</h3>
        <p>A <strong>Higher-Order Function (HOF)</strong> is a function that either:</p>
        <ul>
            <li>Takes a function as an argument, OR</li>
            <li>Returns a function as its result</li>
        </ul>

        <h4>Examples You Already Use</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// .map(), .filter(), .reduce() are all HOFs</span>
<span style="color:#569cd6;">const</span> nums = [1, 2, 3, 4, 5];
<span style="color:#569cd6;">const</span> doubled = nums.map(n => n * 2);       <span style="color:#6a9955;">// [2, 4, 6, 8, 10]</span>
<span style="color:#569cd6;">const</span> evens = nums.filter(n => n % 2 === 0); <span style="color:#6a9955;">// [2, 4]</span>
<span style="color:#569cd6;">const</span> sum = nums.reduce((acc, n) => acc + n, 0); <span style="color:#6a9955;">// 15</span>
        </pre>

        <h4>Building Your Own HOF</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> withLogging(fn) {
    <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span>(...args) {
        console.log(<span style="color:#ce9178;">`Calling </span><span style="color:#569cd6;">${fn.name}</span><span style="color:#ce9178;"> with`</span>, args);
        <span style="color:#569cd6;">const</span> result = fn(...args);
        console.log(<span style="color:#ce9178;">`Result:`</span>, result);
        <span style="color:#569cd6;">return</span> result;
    };
}

<span style="color:#569cd6;">const</span> add = (a, b) => a + b;
<span style="color:#569cd6;">const</span> loggedAdd = withLogging(add);
loggedAdd(2, 3); <span style="color:#6a9955;">// "Calling add with [2, 3]" → "Result: 5"</span>
        </pre>

        <h4>Function Composition</h4>
        <p>Combining small functions to build complex behavior:</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> compose = (...fns) => (x) => fns.reduceRight((acc, fn) => fn(acc), x);
<span style="color:#569cd6;">const</span> pipe    = (...fns) => (x) => fns.reduce((acc, fn) => fn(acc), x);

<span style="color:#569cd6;">const</span> double = x => x * 2;
<span style="color:#569cd6;">const</span> addOne = x => x + 1;
<span style="color:#569cd6;">const</span> square = x => x * x;

<span style="color:#569cd6;">const</span> transform = pipe(double, addOne, square);
transform(3); <span style="color:#6a9955;">// 3 → double(3)=6 → addOne(6)=7 → square(7)=49</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the difference between <code>compose</code> and <code>pipe</code>?</li>
            <li>Is <code>Array.prototype.map</code> a higher-order function? Why?</li>
            <li>Write a <code>repeat(fn, n)</code> HOF that calls <code>fn</code> exactly <code>n</code> times.</li>
        </ol>
        """
    },
    {
        "day": 17,
        "phase": "Phase 4: Advanced Functions",
        "title": "Pure Functions & Side Effects",
        "content": """
        <h3>The foundation of predictable code</h3>
        <p>A <strong>Pure Function</strong> has two properties:</p>
        <ol>
            <li><strong>Deterministic:</strong> Same input ALWAYS produces same output.</li>
            <li><strong>No Side Effects:</strong> It does not modify anything outside itself.</li>
        </ol>

        <h4>Pure vs Impure</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// ✅ PURE: Depends only on inputs, changes nothing outside</span>
<span style="color:#569cd6;">function</span> add(a, b) { <span style="color:#569cd6;">return</span> a + b; }
<span style="color:#569cd6;">function</span> toUpper(str) { <span style="color:#569cd6;">return</span> str.toUpperCase(); }

<span style="color:#6a9955;">// ❌ IMPURE: Modifies external state</span>
<span style="color:#569cd6;">let</span> total = 0;
<span style="color:#569cd6;">function</span> addToTotal(x) { total += x; <span style="color:#569cd6;">return</span> total; }

<span style="color:#6a9955;">// ❌ IMPURE: Non-deterministic (different output each call)</span>
<span style="color:#569cd6;">function</span> now() { <span style="color:#569cd6;">return</span> Date.now(); }

<span style="color:#6a9955;">// ❌ IMPURE: Side effect (console output, DOM manipulation, HTTP request)</span>
<span style="color:#569cd6;">function</span> logName(name) { console.log(name); }
        </pre>

        <h4>Why This Matters</h4>
        <ul>
            <li><strong>Testability:</strong> Pure functions need no mocks or setup. Just pass input, assert output.</li>
            <li><strong>Cacheability:</strong> Since output depends only on input, results can be memoized.</li>
            <li><strong>Parallelization:</strong> Pure functions can run in parallel without race conditions.</li>
            <li><strong>Referential Transparency:</strong> You can replace <code>add(2,3)</code> with <code>5</code> anywhere without changing behavior.</li>
        </ul>

        <h4>Avoiding Mutation</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// ❌ Mutates the original array</span>
<span style="color:#569cd6;">function</span> addItem(arr, item) { arr.push(item); <span style="color:#569cd6;">return</span> arr; }

<span style="color:#6a9955;">// ✅ Returns a NEW array</span>
<span style="color:#569cd6;">function</span> addItem(arr, item) { <span style="color:#569cd6;">return</span> [...arr, item]; }
        </pre>
        """,
        "quiz": """
        <ol>
            <li>Is <code>Math.random()</code> a pure function? Why?</li>
            <li>Can a function that reads from the DOM be pure? Explain.</li>
            <li>Rewrite this impure function as pure: <code>let count = 0; function increment() { count++; return count; }</code></li>
        </ol>
        """
    },
    {
        "day": 18,
        "phase": "Phase 4: Advanced Functions",
        "title": "Currying & Partial Application",
        "content": """
        <h3>Transforming functions for reusability</h3>

        <h4>Currying</h4>
        <p>Currying transforms a function with multiple arguments into a sequence of functions that each take one argument.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Normal function</span>
<span style="color:#569cd6;">function</span> add(a, b, c) { <span style="color:#569cd6;">return</span> a + b + c; }
add(1, 2, 3); <span style="color:#6a9955;">// 6</span>

<span style="color:#6a9955;">// Curried version</span>
<span style="color:#569cd6;">function</span> curriedAdd(a) {
    <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span>(b) {
        <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span>(c) {
            <span style="color:#569cd6;">return</span> a + b + c;
        };
    };
}
curriedAdd(1)(2)(3); <span style="color:#6a9955;">// 6</span>

<span style="color:#6a9955;">// Arrow function version</span>
<span style="color:#569cd6;">const</span> curriedAdd = a => b => c => a + b + c;
        </pre>

        <h4>Generic Curry Utility</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> curry(fn) {
    <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span> curried(...args) {
        <span style="color:#569cd6;">if</span> (args.length >= fn.length) {
            <span style="color:#569cd6;">return</span> fn.apply(<span style="color:#569cd6;">this</span>, args);
        }
        <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span>(...args2) {
            <span style="color:#569cd6;">return</span> curried.apply(<span style="color:#569cd6;">this</span>, args.concat(args2));
        };
    };
}

<span style="color:#569cd6;">const</span> sum = curry((a, b, c) => a + b + c);
sum(1)(2)(3);    <span style="color:#6a9955;">// 6</span>
sum(1, 2)(3);    <span style="color:#6a9955;">// 6</span>
sum(1)(2, 3);    <span style="color:#6a9955;">// 6</span>
        </pre>

        <h4>Practical Use Case</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> log = curry((level, timestamp, message) => {
    console.log(<span style="color:#ce9178;">`[</span><span style="color:#569cd6;">${level}</span><span style="color:#ce9178;">] </span><span style="color:#569cd6;">${timestamp}</span><span style="color:#ce9178;">: </span><span style="color:#569cd6;">${message}</span><span style="color:#ce9178;">`</span>);
});

<span style="color:#569cd6;">const</span> errorLog = log("ERROR");           <span style="color:#6a9955;">// Partially applied</span>
<span style="color:#569cd6;">const</span> todayError = errorLog("2024-01-01"); <span style="color:#6a9955;">// More partial</span>
todayError("Server crashed");             <span style="color:#6a9955;">// "[ERROR] 2024-01-01: Server crashed"</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the difference between Currying and Partial Application?</li>
            <li>What does <code>fn.length</code> return, and why is it important in the curry utility?</li>
            <li>Write a curried function <code>multiply</code> such that <code>multiply(2)(3)(4)</code> returns <code>24</code>.</li>
        </ol>
        """
    },
    {
        "day": 19,
        "phase": "Phase 4: Advanced Functions",
        "title": "Recursion & Tail Call Optimization",
        "content": """
        <h3>When a function calls itself</h3>
        <p>Recursion needs two things: a <strong>base case</strong> (when to stop) and a <strong>recursive case</strong> (the self-call).</p>

        <h4>Classic Example: Factorial</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> factorial(n) {
    <span style="color:#569cd6;">if</span> (n <= 1) <span style="color:#569cd6;">return</span> 1;     <span style="color:#6a9955;">// Base case</span>
    <span style="color:#569cd6;">return</span> n * factorial(n - 1); <span style="color:#6a9955;">// Recursive case</span>
}
<span style="color:#6a9955;">// factorial(5) → 5 * factorial(4) → 5 * 4 * factorial(3) → ...
// Each call ADDS to the call stack. factorial(10000) = Stack Overflow!</span>
        </pre>

        <h4>Tail Call Optimization (TCO)</h4>
        <p>A <strong>tail call</strong> is when the recursive call is the LAST operation in the function 
        (no multiplication after). This allows the engine to reuse the current stack frame.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Tail-recursive version</span>
<span style="color:#569cd6;">function</span> factorial(n, accumulator = 1) {
    <span style="color:#569cd6;">if</span> (n <= 1) <span style="color:#569cd6;">return</span> accumulator;
    <span style="color:#569cd6;">return</span> factorial(n - 1, n * accumulator); <span style="color:#6a9955;">// Tail position!</span>
}
<span style="color:#6a9955;">// Note: Only Safari implements TCO. V8 does NOT.</span>
        </pre>

        <h4>Converting Recursion to Iteration (Safer)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Trampoline pattern: avoids stack overflow</span>
<span style="color:#569cd6;">function</span> trampoline(fn) {
    <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">function</span>(...args) {
        <span style="color:#569cd6;">let</span> result = fn(...args);
        <span style="color:#569cd6;">while</span> (<span style="color:#569cd6;">typeof</span> result === 'function') {
            result = result();
        }
        <span style="color:#569cd6;">return</span> result;
    };
}

<span style="color:#569cd6;">function</span> factorial(n, acc = 1) {
    <span style="color:#569cd6;">if</span> (n <= 1) <span style="color:#569cd6;">return</span> acc;
    <span style="color:#569cd6;">return</span> () => factorial(n - 1, n * acc); <span style="color:#6a9955;">// Returns a function, not a call</span>
}

<span style="color:#569cd6;">const</span> safeFactorial = trampoline(factorial);
safeFactorial(100000); <span style="color:#6a9955;">// No stack overflow! ✅</span>
        </pre>

        <h4>Real Use Cases for Recursion</h4>
        <p>Tree traversal (DOM, file systems), JSON deep clone, flattening nested arrays, parsing nested structures.</p>
        """,
        "quiz": """
        <ol>
            <li>Why does V8 (Chrome/Node) NOT implement Tail Call Optimization? (Hint: debugging)</li>
            <li>Convert this recursive Fibonacci function to use the Trampoline pattern.</li>
            <li>Write a recursive function to deep-flatten an array: <code>[1, [2, [3, [4]]]]</code> → <code>[1, 2, 3, 4]</code></li>
        </ol>
        """
    },
    {
        "day": 20,
        "phase": "Phase 4: Advanced Functions",
        "title": "Generator Functions & Iterators",
        "content": """
        <h3>Functions that can pause and resume</h3>
        <p>A Generator function can stop midway through execution, yield a value, and later resume from where it left off.</p>

        <h4>Syntax</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function*</span> countUp() {
    <span style="color:#569cd6;">yield</span> 1;
    <span style="color:#569cd6;">yield</span> 2;
    <span style="color:#569cd6;">yield</span> 3;
}

<span style="color:#569cd6;">const</span> gen = countUp(); <span style="color:#6a9955;">// Does NOT run the function! Returns an iterator.</span>
gen.next(); <span style="color:#6a9955;">// { value: 1, done: false }</span>
gen.next(); <span style="color:#6a9955;">// { value: 2, done: false }</span>
gen.next(); <span style="color:#6a9955;">// { value: 3, done: false }</span>
gen.next(); <span style="color:#6a9955;">// { value: undefined, done: true }</span>
        </pre>

        <h4>The Iterator Protocol</h4>
        <p>Any object with a <code>next()</code> method that returns <code>{ value, done }</code> is an iterator. 
        Generators automatically implement this protocol.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Custom iterable using Symbol.iterator</span>
<span style="color:#569cd6;">const</span> range = {
    from: 1,
    to: 5,
    [Symbol.iterator]() {
        <span style="color:#569cd6;">let</span> current = <span style="color:#569cd6;">this</span>.from;
        <span style="color:#569cd6;">const</span> last = <span style="color:#569cd6;">this</span>.to;
        <span style="color:#569cd6;">return</span> {
            next() {
                <span style="color:#569cd6;">return</span> current <= last
                    ? { value: current++, done: <span style="color:#569cd6;">false</span> }
                    : { done: <span style="color:#569cd6;">true</span> };
            }
        };
    }
};
<span style="color:#569cd6;">for</span> (<span style="color:#569cd6;">const</span> num <span style="color:#569cd6;">of</span> range) console.log(num); <span style="color:#6a9955;">// 1, 2, 3, 4, 5</span>
        </pre>

        <h4>Infinite Sequences</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function*</span> fibonacci() {
    <span style="color:#569cd6;">let</span> a = 0, b = 1;
    <span style="color:#569cd6;">while</span> (<span style="color:#569cd6;">true</span>) { <span style="color:#6a9955;">// Infinite! But safe because it's lazy.</span>
        <span style="color:#569cd6;">yield</span> a;
        [a, b] = [b, a + b];
    }
}
<span style="color:#569cd6;">const</span> fib = fibonacci();
fib.next().value; <span style="color:#6a9955;">// 0</span>
fib.next().value; <span style="color:#6a9955;">// 1</span>
fib.next().value; <span style="color:#6a9955;">// 1</span>
fib.next().value; <span style="color:#6a9955;">// 2</span>
        </pre>

        <h4>Two-Way Communication</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function*</span> conversation() {
    <span style="color:#569cd6;">const</span> name = <span style="color:#569cd6;">yield</span> "What is your name?";
    <span style="color:#569cd6;">const</span> age = <span style="color:#569cd6;">yield</span> <span style="color:#ce9178;">`Hello </span><span style="color:#569cd6;">${name}</span><span style="color:#ce9178;">! How old are you?`</span>;
    <span style="color:#569cd6;">yield</span> <span style="color:#ce9178;">`</span><span style="color:#569cd6;">${name}</span><span style="color:#ce9178;"> is </span><span style="color:#569cd6;">${age}</span><span style="color:#ce9178;"> years old.`</span>;
}
<span style="color:#569cd6;">const</span> chat = conversation();
chat.next();          <span style="color:#6a9955;">// { value: "What is your name?" }</span>
chat.next("Alice");   <span style="color:#6a9955;">// { value: "Hello Alice! How old are you?" }</span>
chat.next(30);        <span style="color:#6a9955;">// { value: "Alice is 30 years old." }</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the difference between a Generator and a regular function in terms of memory?</li>
            <li>What does <code>yield</code> do differently from <code>return</code>?</li>
            <li>How are Generators related to <code>async/await</code>? (Hint: async/await is built on top of generators)</li>
        </ol>
        """
    },

    # ===================================================
    # PHASE 5: ASYNC JAVASCRIPT (Day 21-25)
    # ===================================================
    {
        "day": 21,
        "phase": "Phase 5: Async JavaScript",
        "title": "The Event Loop & Concurrency Model",
        "content": """
        <h3>How single-threaded JS handles async operations</h3>
        <p>JS has ONE thread, ONE call stack, but it can handle thousands of async operations. 
        The secret: the <strong>Event Loop</strong> + <strong>Web APIs</strong> + <strong>Callback Queue</strong>.</p>

        <h4>The Architecture</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
┌───────────────┐   ┌───────────────┐
│  Call Stack    │   │   Web APIs    │
│ (Your JS code)│──→│ (setTimeout,  │
│               │   │  fetch, DOM)  │
└───────┬───────┘   └───────┬───────┘
        │                   │
        │           ┌───────▼───────┐
        │           │ Callback Queue │
        │           │ (Task Queue)   │
        │           └───────┬───────┘
        │                   │
        └───────────────────┘
          Event Loop checks:
          "Is the Call Stack empty?
           If yes, push next callback."
        </pre>

        <h4>Step-by-Step Example</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
console.log("1");

setTimeout(() => {
    console.log("2");
}, 0); <span style="color:#6a9955;">// 0ms delay! But still async.</span>

console.log("3");

<span style="color:#6a9955;">// Output: "1", "3", "2"
// Why? setTimeout callback goes to the Web API, then the Callback Queue.
// The Event Loop waits until "1" and "3" finish (stack is empty),
// THEN pushes the callback.</span>
        </pre>

        <h4>Key Rule</h4>
        <p>The Event Loop will NEVER push a callback from the queue if the Call Stack is not empty. 
        This is why a <code>while(true)</code> loop freezes the browser — the stack is never empty, 
        so no callbacks can run.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// This setTimeout will NEVER fire!</span>
setTimeout(() => console.log("I'm stuck"), 0);
<span style="color:#569cd6;">while</span>(<span style="color:#569cd6;">true</span>) {} <span style="color:#6a9955;">// Stack is never empty. Event Loop is blocked.</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>Why does <code>setTimeout(fn, 0)</code> not execute immediately?</li>
            <li>Is <code>setTimeout</code> part of JavaScript? Or is it a Web API?</li>
            <li>What would happen if you put a very CPU-heavy computation (e.g., sorting 10 million items) on the main thread? How would it affect UI?</li>
        </ol>
        """
    },
    {
        "day": 22,
        "phase": "Phase 5: Async JavaScript",
        "title": "Promises: Internal Mechanics",
        "content": """
        <h3>A Promise is a state machine</h3>
        <p>A Promise is an object representing the eventual completion (or failure) of an async operation. 
        It has 3 states:</p>
        <ul>
            <li><strong>Pending:</strong> Initial state. Neither fulfilled nor rejected.</li>
            <li><strong>Fulfilled:</strong> Operation completed. <code>.then()</code> handlers run.</li>
            <li><strong>Rejected:</strong> Operation failed. <code>.catch()</code> handlers run.</li>
        </ul>
        <p>Once settled (fulfilled or rejected), a promise <strong>cannot change state</strong>.</p>

        <h4>Creating Promises</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> promise = <span style="color:#569cd6;">new</span> Promise((resolve, reject) => {
    <span style="color:#6a9955;">// The executor runs SYNCHRONOUSLY</span>
    <span style="color:#569cd6;">const</span> success = <span style="color:#569cd6;">true</span>;
    <span style="color:#569cd6;">if</span> (success) resolve("Data loaded");
    <span style="color:#569cd6;">else</span> reject(<span style="color:#569cd6;">new</span> Error("Failed"));
});

promise
    .then(data => console.log(data))   <span style="color:#6a9955;">// "Data loaded"</span>
    .catch(err => console.error(err));
        </pre>

        <h4>Chaining: Each <code>.then()</code> returns a NEW Promise</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
fetch('/api/user')
    .then(res => res.json())          <span style="color:#6a9955;">// Returns new Promise with parsed data</span>
    .then(user => fetch(<span style="color:#ce9178;">`/api/posts/</span><span style="color:#569cd6;">${user.id}</span><span style="color:#ce9178;">`</span>)) <span style="color:#6a9955;">// Returns new Promise</span>
    .then(res => res.json())
    .then(posts => console.log(posts))
    .catch(err => console.error(err)); <span style="color:#6a9955;">// Catches ANY error in the chain</span>
        </pre>

        <h4>Promise Static Methods</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Wait for ALL to succeed (fails if ANY rejects)</span>
Promise.all([p1, p2, p3]).then(([r1, r2, r3]) => {});

<span style="color:#6a9955;">// Wait for ALL to settle (never rejects)</span>
Promise.allSettled([p1, p2]).then(results => {
    <span style="color:#6a9955;">// [{ status: "fulfilled", value: ... }, { status: "rejected", reason: ... }]</span>
});

<span style="color:#6a9955;">// First to settle wins (fulfilled OR rejected)</span>
Promise.race([p1, p2]).then(first => {});

<span style="color:#6a9955;">// First to FULFILL wins (ignores rejections)</span>
Promise.any([p1, p2]).then(first => {});
        </pre>
        """,
        "quiz": """
        <ol>
            <li>Does the executor function inside <code>new Promise(executor)</code> run synchronously or asynchronously?</li>
            <li>What is the difference between <code>Promise.all</code> and <code>Promise.allSettled</code>?</li>
            <li>What happens if you don't attach a <code>.catch()</code> to a rejected promise?</li>
        </ol>
        """
    },
    {
        "day": 23,
        "phase": "Phase 5: Async JavaScript",
        "title": "Microtask vs Macrotask Queue",
        "content": """
        <h3>Not all async callbacks are treated equally</h3>
        <p>The Event Loop has TWO queues, and <strong>Microtasks always run before Macrotasks</strong>.</p>

        <h4>Macrotask Queue (Task Queue)</h4>
        <p>Sources: <code>setTimeout</code>, <code>setInterval</code>, <code>setImmediate</code> (Node), I/O, UI rendering.</p>

        <h4>Microtask Queue</h4>
        <p>Sources: <code>Promise.then/catch/finally</code>, <code>queueMicrotask()</code>, <code>MutationObserver</code>.</p>

        <h4>Execution Order</h4>
        <ol>
            <li>Execute ALL synchronous code (Call Stack).</li>
            <li>Drain the ENTIRE Microtask queue.</li>
            <li>Execute ONE Macrotask.</li>
            <li>Drain the ENTIRE Microtask queue again.</li>
            <li>Repeat from step 3.</li>
        </ol>

        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
console.log("1"); <span style="color:#6a9955;">// Sync</span>

setTimeout(() => console.log("2"), 0); <span style="color:#6a9955;">// Macrotask</span>

Promise.resolve().then(() => console.log("3")); <span style="color:#6a9955;">// Microtask</span>

Promise.resolve().then(() => {
    console.log("4"); <span style="color:#6a9955;">// Microtask</span>
    setTimeout(() => console.log("5"), 0); <span style="color:#6a9955;">// Macrotask (queued from microtask)</span>
});

console.log("6"); <span style="color:#6a9955;">// Sync</span>

<span style="color:#6a9955;">// Output: 1, 6, 3, 4, 2, 5
// Step 1: Sync → "1", "6"
// Step 2: Microtasks → "3", "4"
// Step 3: One Macrotask → "2"
// Step 4: Microtasks → (none)
// Step 5: One Macrotask → "5"</span>
        </pre>

        <h4>Why This Matters</h4>
        <p>If you create microtasks inside microtasks infinitely, the macrotask queue (including UI rendering) 
        will STARVE. The page will freeze.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// ❌ DANGER: Infinite microtask loop</span>
<span style="color:#569cd6;">function</span> loop() {
    Promise.resolve().then(loop);
}
loop(); <span style="color:#6a9955;">// Page freezes! Microtask queue never empties.</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is the output? <code>setTimeout(() => console.log('a'), 0); Promise.resolve().then(() => console.log('b')); console.log('c');</code></li>
            <li>Why do Microtasks have higher priority than Macrotasks?</li>
            <li>Can starving the Macrotask queue prevent the browser from rendering? Why?</li>
        </ol>
        """
    },
    {
        "day": 24,
        "phase": "Phase 5: Async JavaScript",
        "title": "async/await Under The Hood",
        "content": """
        <h3><code>async/await</code> is syntactic sugar over Promises + Generators</h3>
        <p>When you write <code>async/await</code>, the engine transforms it into Promise chains internally.</p>

        <h4>What <code>async</code> does</h4>
        <p>Wraps the function's return value in a Promise automatically.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">async function</span> greet() { <span style="color:#569cd6;">return</span> "Hello"; }
<span style="color:#6a9955;">// Equivalent to:</span>
<span style="color:#569cd6;">function</span> greet() { <span style="color:#569cd6;">return</span> Promise.resolve("Hello"); }

greet().then(msg => console.log(msg)); <span style="color:#6a9955;">// "Hello"</span>
        </pre>

        <h4>What <code>await</code> does</h4>
        <p><code>await</code> pauses the async function, unwraps the Promise, and resumes when it settles. 
        Crucially, it yields control back to the Event Loop while waiting.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">async function</span> fetchUser() {
    console.log("A");
    <span style="color:#569cd6;">const</span> res = <span style="color:#569cd6;">await</span> fetch('/api/user'); <span style="color:#6a9955;">// Pauses here</span>
    console.log("B"); <span style="color:#6a9955;">// Resumes after fetch completes</span>
    <span style="color:#569cd6;">return</span> res.json();
}

<span style="color:#6a9955;">// Under the hood, it's like:</span>
<span style="color:#569cd6;">function</span> fetchUser() {
    console.log("A");
    <span style="color:#569cd6;">return</span> fetch('/api/user')
        .then(res => {
            console.log("B");
            <span style="color:#569cd6;">return</span> res.json();
        });
}
        </pre>

        <h4>Common Patterns</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Sequential (slow — each waits for the previous)</span>
<span style="color:#569cd6;">const</span> user = <span style="color:#569cd6;">await</span> fetchUser();
<span style="color:#569cd6;">const</span> posts = <span style="color:#569cd6;">await</span> fetchPosts(user.id);

<span style="color:#6a9955;">// Parallel (fast — both run at the same time)</span>
<span style="color:#569cd6;">const</span> [user, posts] = <span style="color:#569cd6;">await</span> Promise.all([
    fetchUser(),
    fetchPosts()
]);

<span style="color:#6a9955;">// Error handling</span>
<span style="color:#569cd6;">try</span> {
    <span style="color:#569cd6;">const</span> data = <span style="color:#569cd6;">await</span> riskyOperation();
} <span style="color:#569cd6;">catch</span> (err) {
    console.error("Failed:", err.message);
} <span style="color:#569cd6;">finally</span> {
    cleanup();
}
        </pre>

        <h4>Top-Level Await</h4>
        <p>In ES Modules (not CommonJS), you can use <code>await</code> at the top level without wrapping in an async function.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// In a .mjs file or type="module" script</span>
<span style="color:#569cd6;">const</span> data = <span style="color:#569cd6;">await</span> fetch('/api').then(r => r.json());
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What happens to the code AFTER an <code>await</code> statement — does it go to the Microtask or Macrotask queue?</li>
            <li>Why is <code>await</code> in a loop (sequential) slower than <code>Promise.all()</code> (parallel)?</li>
            <li>Can you use <code>await</code> inside a regular (non-async) function? What error do you get?</li>
        </ol>
        """
    },
    {
        "day": 25,
        "phase": "Phase 5: Async JavaScript",
        "title": "Async Error Handling Patterns",
        "content": """
        <h3>Errors in async code behave differently</h3>
        <p>Unlike synchronous errors, async errors can be silently swallowed if not caught properly.</p>

        <h4>The Unhandled Rejection Problem</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// ❌ This rejection is UNHANDLED — crashes Node.js!</span>
<span style="color:#569cd6;">async function</span> fail() { <span style="color:#569cd6;">throw new</span> Error("oops"); }
fail(); <span style="color:#6a9955;">// No .catch(), no try/catch → Unhandled Promise Rejection</span>

<span style="color:#6a9955;">// ✅ Fix 1: try/catch</span>
<span style="color:#569cd6;">try</span> { <span style="color:#569cd6;">await</span> fail(); } <span style="color:#569cd6;">catch</span> (e) { console.error(e); }

<span style="color:#6a9955;">// ✅ Fix 2: .catch()</span>
fail().catch(e => console.error(e));
        </pre>

        <h4>Global Error Handlers</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Browser</span>
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled:', event.reason);
    event.preventDefault(); <span style="color:#6a9955;">// Prevents default logging</span>
});

<span style="color:#6a9955;">// Node.js</span>
process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled:', reason);
});
        </pre>

        <h4>Error-First Pattern (Inspired by Go)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// Utility: wraps async functions to return [error, data]</span>
<span style="color:#569cd6;">async function</span> to(promise) {
    <span style="color:#569cd6;">try</span> {
        <span style="color:#569cd6;">const</span> data = <span style="color:#569cd6;">await</span> promise;
        <span style="color:#569cd6;">return</span> [<span style="color:#569cd6;">null</span>, data];
    } <span style="color:#569cd6;">catch</span> (err) {
        <span style="color:#569cd6;">return</span> [err, <span style="color:#569cd6;">null</span>];
    }
}

<span style="color:#6a9955;">// Usage: Clean, no try/catch blocks everywhere</span>
<span style="color:#569cd6;">const</span> [err, user] = <span style="color:#569cd6;">await</span> to(fetchUser());
<span style="color:#569cd6;">if</span> (err) {
    console.error("Failed:", err);
    <span style="color:#569cd6;">return</span>;
}
console.log(user);
        </pre>

        <h4>Retry Pattern</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">async function</span> retry(fn, retries = 3, delay = 1000) {
    <span style="color:#569cd6;">for</span> (<span style="color:#569cd6;">let</span> i = 0; i < retries; i++) {
        <span style="color:#569cd6;">try</span> {
            <span style="color:#569cd6;">return await</span> fn();
        } <span style="color:#569cd6;">catch</span> (err) {
            <span style="color:#569cd6;">if</span> (i === retries - 1) <span style="color:#569cd6;">throw</span> err;
            console.log(<span style="color:#ce9178;">`Retry </span><span style="color:#569cd6;">${i+1}</span><span style="color:#ce9178;">...</span><span style="color:#ce9178;">`</span>);
            <span style="color:#569cd6;">await new</span> Promise(r => setTimeout(r, delay));
        }
    }
}
<span style="color:#569cd6;">const</span> data = <span style="color:#569cd6;">await</span> retry(() => fetch('/unstable-api'));
        </pre>
        """,
        "quiz": """
        <ol>
            <li>What is an "Unhandled Promise Rejection" and why is it dangerous in Node.js?</li>
            <li>Implement the <code>to()</code> utility function from scratch.</li>
            <li>In the retry pattern, why do we use <code>await new Promise(r => setTimeout(r, delay))</code> instead of just <code>setTimeout</code>?</li>
        </ol>
        """
    },

    # ===================================================
    # PHASE 6: PERFORMANCE & PATTERNS (Day 26-30)
    # ===================================================
    {
        "day": 26,
        "phase": "Phase 6: Performance & Patterns",
        "title": "V8 Hidden Classes & Inline Caching",
        "content": """
        <h3>How V8 makes property access fast</h3>
        <p>Accessing <code>obj.x</code> in a dynamic language like JS should be slow (hash table lookup). 
        V8 uses two tricks to make it nearly as fast as C++.</p>

        <h4>Hidden Classes (Shapes / Maps)</h4>
        <p>V8 assigns a <strong>Hidden Class</strong> to every object. Objects with the same properties 
        added in the same order share the same Hidden Class.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// ✅ GOOD: Same property order → same Hidden Class</span>
<span style="color:#569cd6;">function</span> Point(x, y) {
    <span style="color:#569cd6;">this</span>.x = x; <span style="color:#6a9955;">// Hidden Class C0 → C1 (added x)</span>
    <span style="color:#569cd6;">this</span>.y = y; <span style="color:#6a9955;">// Hidden Class C1 → C2 (added y)</span>
}
<span style="color:#569cd6;">const</span> p1 = <span style="color:#569cd6;">new</span> Point(1, 2); <span style="color:#6a9955;">// Hidden Class: C2</span>
<span style="color:#569cd6;">const</span> p2 = <span style="color:#569cd6;">new</span> Point(3, 4); <span style="color:#6a9955;">// Hidden Class: C2 (same!)</span>

<span style="color:#6a9955;">// ❌ BAD: Different property order → different Hidden Classes</span>
<span style="color:#569cd6;">const</span> a = {}; a.x = 1; a.y = 2; <span style="color:#6a9955;">// Class: {x,y}</span>
<span style="color:#569cd6;">const</span> b = {}; b.y = 2; b.x = 1; <span style="color:#6a9955;">// Class: {y,x} — DIFFERENT!</span>
        </pre>

        <h4>Inline Caching (IC)</h4>
        <p>When a function accesses <code>obj.x</code>, V8 caches the Hidden Class and the memory offset. 
        Next time the same function runs with an object of the same Hidden Class, it skips the lookup entirely.</p>
        <ul>
            <li><strong>Monomorphic:</strong> Always the same Hidden Class → fastest (1 cache entry).</li>
            <li><strong>Polymorphic:</strong> 2-4 different classes → slower (multiple cache entries).</li>
            <li><strong>Megamorphic:</strong> 5+ classes → slowest (cache abandoned, full lookup).</li>
        </ul>

        <h4>Performance Tips</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// ✅ Initialize all properties in the constructor</span>
<span style="color:#569cd6;">function</span> User(name, age) {
    <span style="color:#569cd6;">this</span>.name = name;
    <span style="color:#569cd6;">this</span>.age = age;
    <span style="color:#569cd6;">this</span>.email = <span style="color:#569cd6;">null</span>; <span style="color:#6a9955;">// Even if unknown, declare it!</span>
}

<span style="color:#6a9955;">// ❌ Don't add properties later dynamically</span>
<span style="color:#569cd6;">const</span> u = <span style="color:#569cd6;">new</span> User("Alice", 30);
u.phone = "123"; <span style="color:#6a9955;">// Creates a NEW Hidden Class → deoptimizes</span>

<span style="color:#6a9955;">// ❌ Don't delete properties</span>
<span style="color:#569cd6;">delete</span> u.age; <span style="color:#6a9955;">// Forces Hidden Class change → slow</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>Why does adding properties in a different order to two objects make V8 slower?</li>
            <li>What is the difference between Monomorphic, Polymorphic, and Megamorphic inline caches?</li>
            <li>Why should you avoid using <code>delete</code> on object properties in performance-critical code?</li>
        </ol>
        """
    },
    {
        "day": 27,
        "phase": "Phase 6: Performance & Patterns",
        "title": "Proxy & Reflect",
        "content": """
        <h3>Intercepting and customizing object operations</h3>
        <p>A <strong>Proxy</strong> wraps an object and lets you intercept operations like 
        property access, assignment, deletion, function calls, etc.</p>

        <h4>Basic Syntax</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> target = { name: "Alice", age: 30 };

<span style="color:#569cd6;">const</span> handler = {
    get(target, prop) {
        console.log(<span style="color:#ce9178;">`Accessing: </span><span style="color:#569cd6;">${prop}</span><span style="color:#ce9178;">`</span>);
        <span style="color:#569cd6;">return</span> prop <span style="color:#569cd6;">in</span> target ? target[prop] : <span style="color:#ce9178;">"Property not found"</span>;
    },
    set(target, prop, value) {
        <span style="color:#569cd6;">if</span> (prop === 'age' && <span style="color:#569cd6;">typeof</span> value !== 'number') {
            <span style="color:#569cd6;">throw new</span> TypeError("Age must be a number");
        }
        target[prop] = value;
        <span style="color:#569cd6;">return true</span>;
    }
};

<span style="color:#569cd6;">const</span> proxy = <span style="color:#569cd6;">new</span> Proxy(target, handler);
proxy.name;       <span style="color:#6a9955;">// "Accessing: name" → "Alice"</span>
proxy.age = "hi"; <span style="color:#6a9955;">// TypeError: Age must be a number</span>
proxy.unknown;    <span style="color:#6a9955;">// "Property not found"</span>
        </pre>

        <h4>Real-World Use Cases</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// 1. VALIDATION</span>
<span style="color:#569cd6;">const</span> validator = <span style="color:#569cd6;">new</span> Proxy({}, {
    set(obj, prop, val) {
        <span style="color:#569cd6;">if</span> (prop === 'email' && !val.includes('@')) <span style="color:#569cd6;">throw</span> Error('Invalid email');
        obj[prop] = val;
        <span style="color:#569cd6;">return true</span>;
    }
});

<span style="color:#6a9955;">// 2. LOGGING / DEBUGGING</span>
<span style="color:#569cd6;">function</span> createLogged(obj) {
    <span style="color:#569cd6;">return new</span> Proxy(obj, {
        get(t, p) { console.log(<span style="color:#ce9178;">`GET </span><span style="color:#569cd6;">${p}</span><span style="color:#ce9178;">`</span>); <span style="color:#569cd6;">return</span> Reflect.get(t, p); },
        set(t, p, v) { console.log(<span style="color:#ce9178;">`SET </span><span style="color:#569cd6;">${p}</span><span style="color:#ce9178;"> = </span><span style="color:#569cd6;">${v}</span><span style="color:#ce9178;">`</span>); <span style="color:#569cd6;">return</span> Reflect.set(t, p, v); }
    });
}

<span style="color:#6a9955;">// 3. NEGATIVE ARRAY INDICES (like Python!)</span>
<span style="color:#569cd6;">const</span> arr = <span style="color:#569cd6;">new</span> Proxy([1,2,3,4,5], {
    get(target, prop) {
        <span style="color:#569cd6;">const</span> index = Number(prop);
        <span style="color:#569cd6;">if</span> (index < 0) <span style="color:#569cd6;">return</span> target[target.length + index];
        <span style="color:#569cd6;">return</span> Reflect.get(target, prop);
    }
});
arr[-1]; <span style="color:#6a9955;">// 5 (last element!)</span>
        </pre>

        <h4>Reflect</h4>
        <p><code>Reflect</code> provides methods that mirror Proxy traps. It's the "default behavior" 
        you can fall back to inside a handler.</p>
        """,
        "quiz": """
        <ol>
            <li>What is the relationship between <code>Proxy</code> traps and <code>Reflect</code> methods?</li>
            <li>How does Vue.js 3 use Proxy for reactivity (detecting when data changes)?</li>
            <li>Can the target object tell if it's being accessed through a Proxy?</li>
        </ol>
        """
    },
    {
        "day": 28,
        "phase": "Phase 6: Performance & Patterns",
        "title": "WeakMap, WeakSet & Weak References",
        "content": """
        <h3>Data structures that don't prevent garbage collection</h3>
        <p>A regular <code>Map</code> keeps strong references to its keys. 
        Even if nothing else references the key, the Map prevents GC. 
        <code>WeakMap</code> uses <strong>weak references</strong> — if the key is garbage collected, the entry vanishes.</p>

        <h4>WeakMap</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> cache = <span style="color:#569cd6;">new</span> WeakMap();

<span style="color:#569cd6;">function</span> process(obj) {
    <span style="color:#569cd6;">if</span> (cache.has(obj)) <span style="color:#569cd6;">return</span> cache.get(obj);
    <span style="color:#569cd6;">const</span> result = <span style="color:#6a9955;">/* expensive computation */</span> obj.data * 2;
    cache.set(obj, result);
    <span style="color:#569cd6;">return</span> result;
}

<span style="color:#569cd6;">let</span> myObj = { data: 42 };
process(myObj); <span style="color:#6a9955;">// Computed and cached</span>
process(myObj); <span style="color:#6a9955;">// From cache</span>

myObj = <span style="color:#569cd6;">null</span>;   <span style="color:#6a9955;">// myObj is GC'd → WeakMap entry auto-removed! No leak!</span>
        </pre>

        <h4>WeakMap Constraints</h4>
        <ul>
            <li>Keys MUST be objects (not primitives).</li>
            <li>NOT iterable (no <code>.forEach</code>, no <code>.size</code>).</li>
            <li>Cannot be cleared entirely.</li>
        </ul>

        <h4>Real Use Cases</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// 1. PRIVATE DATA (used by many frameworks)</span>
<span style="color:#569cd6;">const</span> privateData = <span style="color:#569cd6;">new</span> WeakMap();

<span style="color:#569cd6;">class</span> User {
    constructor(name, password) {
        <span style="color:#569cd6;">this</span>.name = name;
        privateData.set(<span style="color:#569cd6;">this</span>, { password }); <span style="color:#6a9955;">// Truly private!</span>
    }
    checkPassword(input) {
        <span style="color:#569cd6;">return</span> privateData.get(<span style="color:#569cd6;">this</span>).password === input;
    }
}
<span style="color:#569cd6;">const</span> u = <span style="color:#569cd6;">new</span> User("Alice", "secret123");
u.password;            <span style="color:#6a9955;">// undefined — not on the object</span>
u.checkPassword("secret123"); <span style="color:#6a9955;">// true</span>

<span style="color:#6a9955;">// 2. DOM ELEMENT METADATA</span>
<span style="color:#569cd6;">const</span> metadata = <span style="color:#569cd6;">new</span> WeakMap();
<span style="color:#569cd6;">const</span> btn = document.querySelector('#btn');
metadata.set(btn, { clicks: 0 });
<span style="color:#6a9955;">// If btn is removed from DOM and dereferenced,
// the metadata is automatically cleaned up.</span>
        </pre>

        <h4>WeakSet</h4>
        <p>Same concept: stores objects weakly. Perfect for tracking "has this object been seen before?" 
        without preventing garbage collection.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> visited = <span style="color:#569cd6;">new</span> WeakSet();
<span style="color:#569cd6;">function</span> track(obj) {
    <span style="color:#569cd6;">if</span> (visited.has(obj)) { console.log("Already seen"); <span style="color:#569cd6;">return</span>; }
    visited.add(obj);
    console.log("First visit");
}
        </pre>
        """,
        "quiz": """
        <ol>
            <li>Why can't WeakMap keys be primitive values (strings, numbers)?</li>
            <li>Why is WeakMap not iterable? (Think about what garbage collection means for iteration)</li>
            <li>How would you use a WeakMap to implement a caching decorator for API calls?</li>
        </ol>
        """
    },
    {
        "day": 29,
        "phase": "Phase 6: Performance & Patterns",
        "title": "Web Workers & Multithreading",
        "content": """
        <h3>Running JavaScript off the main thread</h3>
        <p>Heavy computation (image processing, data parsing, crypto) blocks the main thread and freezes the UI. 
        <strong>Web Workers</strong> let you run JS in a separate background thread.</p>

        <h4>Key Constraints</h4>
        <ul>
            <li>Workers have NO access to the DOM.</li>
            <li>Workers have NO access to <code>window</code>, <code>document</code>, or <code>localStorage</code>.</li>
            <li>Communication happens via <strong>message passing</strong> (<code>postMessage</code>).</li>
            <li>Data is COPIED (structured clone), not shared (unless using SharedArrayBuffer).</li>
        </ul>

        <h4>Basic Example</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// main.js</span>
<span style="color:#569cd6;">const</span> worker = <span style="color:#569cd6;">new</span> Worker('worker.js');

worker.postMessage({ numbers: [1,2,3,4,5] }); <span style="color:#6a9955;">// Send data TO worker</span>

worker.onmessage = (event) => {
    console.log("Result:", event.data); <span style="color:#6a9955;">// Receive data FROM worker</span>
};

worker.onerror = (error) => {
    console.error("Worker error:", error.message);
};
        </pre>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#6a9955;">// worker.js</span>
self.onmessage = (event) => {
    <span style="color:#569cd6;">const</span> { numbers } = event.data;
    
    <span style="color:#6a9955;">// Heavy computation happens here — doesn't block UI!</span>
    <span style="color:#569cd6;">const</span> sum = numbers.reduce((a, b) => a + b, 0);
    
    self.postMessage(sum); <span style="color:#6a9955;">// Send result back to main thread</span>
};
        </pre>

        <h4>Inline Worker (No separate file)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> code = <span style="color:#ce9178;">`
    self.onmessage = (e) => {
        const result = e.data * 2;
        self.postMessage(result);
    };
`</span>;
<span style="color:#569cd6;">const</span> blob = <span style="color:#569cd6;">new</span> Blob([code], { type: 'application/javascript' });
<span style="color:#569cd6;">const</span> worker = <span style="color:#569cd6;">new</span> Worker(URL.createObjectURL(blob));
worker.postMessage(21);
worker.onmessage = (e) => console.log(e.data); <span style="color:#6a9955;">// 42</span>
        </pre>

        <h4>Transferable Objects (Zero-Copy)</h4>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">const</span> buffer = <span style="color:#569cd6;">new</span> ArrayBuffer(1024 * 1024); <span style="color:#6a9955;">// 1MB</span>
worker.postMessage(buffer, [buffer]); <span style="color:#6a9955;">// Transfer, not copy!</span>
console.log(buffer.byteLength); <span style="color:#6a9955;">// 0 — ownership transferred to worker</span>
        </pre>
        """,
        "quiz": """
        <ol>
            <li>Why can't a Web Worker access the DOM?</li>
            <li>What is the difference between <code>postMessage</code> (copying) and Transferable Objects?</li>
            <li>When would you use a Web Worker vs. <code>requestIdleCallback</code> for background tasks?</li>
        </ol>
        """
    },
    {
        "day": 30,
        "phase": "Phase 6: Performance & Patterns",
        "title": "Design Patterns: Factory, Observer, Singleton",
        "content": """
        <h3>Reusable solutions to common problems</h3>

        <h4>1. Factory Pattern</h4>
        <p>Creates objects without using <code>new</code>. Useful when object creation is complex or conditional.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">function</span> createUser(type) {
    <span style="color:#569cd6;">switch</span>(type) {
        <span style="color:#569cd6;">case</span> 'admin':
            <span style="color:#569cd6;">return</span> { role: 'admin', permissions: ['read','write','delete'] };
        <span style="color:#569cd6;">case</span> 'viewer':
            <span style="color:#569cd6;">return</span> { role: 'viewer', permissions: ['read'] };
        <span style="color:#569cd6;">default</span>:
            <span style="color:#569cd6;">throw new</span> Error('Unknown type');
    }
}
<span style="color:#569cd6;">const</span> admin = createUser('admin');
        </pre>

        <h4>2. Observer Pattern (Pub/Sub)</h4>
        <p>One-to-many relationship: when one object changes state, all dependents are notified. 
        This is how event systems work.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">class</span> EventEmitter {
    constructor() { <span style="color:#569cd6;">this</span>.events = {}; }
    
    on(event, callback) {
        <span style="color:#569cd6;">if</span> (!<span style="color:#569cd6;">this</span>.events[event]) <span style="color:#569cd6;">this</span>.events[event] = [];
        <span style="color:#569cd6;">this</span>.events[event].push(callback);
        <span style="color:#569cd6;">return</span> <span style="color:#569cd6;">this</span>; <span style="color:#6a9955;">// For chaining</span>
    }
    
    emit(event, ...args) {
        (<span style="color:#569cd6;">this</span>.events[event] || []).forEach(cb => cb(...args));
    }
    
    off(event, callback) {
        <span style="color:#569cd6;">this</span>.events[event] = (<span style="color:#569cd6;">this</span>.events[event] || [])
            .filter(cb => cb !== callback);
    }
}

<span style="color:#569cd6;">const</span> emitter = <span style="color:#569cd6;">new</span> EventEmitter();
emitter.on('userLogin', (user) => console.log(<span style="color:#ce9178;">`Welcome </span><span style="color:#569cd6;">${user}</span><span style="color:#ce9178;">`</span>));
emitter.on('userLogin', (user) => analytics.track(user));
emitter.emit('userLogin', 'Alice'); <span style="color:#6a9955;">// Both handlers fire</span>
        </pre>

        <h4>3. Singleton Pattern</h4>
        <p>Ensures a class has only ONE instance globally.</p>
        <pre style="background:#1e1e1e; color:#d4d4d4; padding:15px; border-radius:6px;">
<span style="color:#569cd6;">class</span> Database {
    constructor() {
        <span style="color:#569cd6;">if</span> (Database.instance) <span style="color:#569cd6;">return</span> Database.instance;
        <span style="color:#569cd6;">this</span>.connection = "connected";
        Database.instance = <span style="color:#569cd6;">this</span>;
    }
}

<span style="color:#569cd6;">const</span> db1 = <span style="color:#569cd6;">new</span> Database();
<span style="color:#569cd6;">const</span> db2 = <span style="color:#569cd6;">new</span> Database();
console.log(db1 === db2); <span style="color:#6a9955;">// true — same instance!</span>

<span style="color:#6a9955;">// Modern ES Module Singleton (simpler):</span>
<span style="color:#6a9955;">// Since ES modules are cached after first import,</span>
<span style="color:#6a9955;">// exporting an instance IS a singleton.</span>
<span style="color:#6a9955;">// db.js</span>
<span style="color:#569cd6;">export const</span> db = <span style="color:#569cd6;">new</span> Database();
        </pre>

        <h3 style="text-align:center; margin-top: 30px;">🎉 Congratulations!</h3>
        <p style="text-align:center;">You have completed the 30-day Advanced JavaScript Deep Dive. 
        You now understand how the engine works internally, how memory is managed, 
        and how to write performant, well-structured code. Keep building!</p>
        """,
        "quiz": """
        <ol>
            <li>What is the main advantage of the Factory Pattern over using <code>new</code> directly?</li>
            <li>How is the Observer Pattern different from simply calling functions directly? What problem does it solve?</li>
            <li>Why is the ES Module singleton considered better than the class-based singleton pattern?</li>
        </ol>
        """
    }
]


# =====================================================
# EMAIL SENDER (No changes needed here)
# =====================================================
def send_daily_lesson():
    today = datetime.now()
    delta = today - COURSE_START_DATE
    day_index = delta.days

    if day_index < 0:
        print("Course hasn't started yet.")
        return

    if day_index >= len(CURRICULUM):
        print(f"Course completed! All {len(CURRICULUM)} days done. Stopping.")
        return

    lesson = CURRICULUM[day_index]
    phase = lesson.get("phase", "")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = f"JS Deep Dive — {lesson['title']}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL

    html_body = f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.7; color: #333; max-width: 700px; margin: auto; padding: 10px;">
        
        <div style="background-color: #f7df1e; padding: 20px; text-align: center; border-radius: 8px 8px 0 0;">
            <h1 style="margin:0; color: #000; font-size: 26px;">JavaScript Daily</h1>
            <p style="margin:5px 0 0 0; color: #555; font-size: 14px;">{phase}</p>
        </div>
        
        <div style="background-color: #fff; padding: 25px; border: 1px solid #eee;">
            <h2 style="color: #2c3e50; border-bottom: 2px solid #f7df1e; padding-bottom: 10px;">{lesson['title']}</h2>
            
            {lesson['content']}
            
            <div style="background-color: #f0f7ff; border-left: 4px solid #3498db; padding: 15px; margin-top: 30px; border-radius: 4px;">
                <h3 style="color: #2980b9; margin-top: 0;">🧠 Daily Quiz</h3>
                {lesson['quiz']}
                <p style="font-style: italic; color: #777; font-size: 12px;">Try to answer before looking anything up. Write your answers down.</p>
            </div>
        </div>

        <div style="text-align: center; padding: 15px; font-size: 13px; color: #888; background-color: #f9f9f9; border-radius: 0 0 8px 8px; border: 1px solid #eee; border-top: 0;">
            Day {day_index + 1} of {len(CURRICULUM)} • Automated via GitHub Actions
        </div>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, EMAIL_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print(f"✅ Sent: {lesson['title']} (Day {day_index + 1}/{len(CURRICULUM)})")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    send_daily_lesson()
