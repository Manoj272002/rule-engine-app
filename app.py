from flask import Flask, request, jsonify, render_template_string
import ast
import operator as op
import threading

# ASTNode class for representing rule nodes
class ASTNode:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.node_type = node_type  # "operator" or "operand"
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return f"{self.node_type}: {self.value}"

# Function to create the AST (rule creation)
def create_rule(rule_string):
    # Supported operators for evaluation
    operators = {
        ast.And: lambda x, y: x and y,
        ast.Or: lambda x, y: x or y,
        ast.Eq: op.eq,
        ast.NotEq: op.ne,
        ast.Gt: op.gt,
        ast.Lt: op.lt,
        ast.GtE: op.ge,
        ast.LtE: op.le,
    }

    class RuleTransformer(ast.NodeTransformer):
        def visit_Compare(self, node):
            left = self.visit(node.left)
            right = self.visit(node.comparators[0])
            op_type = type(node.ops[0])
            return ASTNode("operand", value=(left.id, operators[op_type], right.n))

        def visit_BoolOp(self, node):
            op_type = type(node.op)
            operator = "AND" if op_type is ast.And else "OR"
            left = self.visit(node.values[0])
            right = self.visit(node.values[1])
            return ASTNode("operator", left=left, right=right, value=operator)

    # Parse the rule into an AST
    tree = ast.parse(rule_string, mode='eval')
    return RuleTransformer().visit(tree.body)

# Function to evaluate the rule against provided data
def evaluate_rule(ast_tree, data):
    if ast_tree.node_type == "operator":
        left_result = evaluate_rule(ast_tree.left, data)
        right_result = evaluate_rule(ast_tree.right, data)
        if ast_tree.value == "AND":
            return left_result and right_result
        elif ast_tree.value == "OR":
            return left_result or right_result
    elif ast_tree.node_type == "operand":
        left, operator_func, right = ast_tree.value
        return operator_func(data[left], right)

# Create a Flask app
app = Flask(__name__)

# Global variable to store the rule AST
global_rule_ast = None

# Route for home page with form inputs
@app.route('/')
def home():
    return render_template_string('''
        <style>
            body { background-color: #e0f7fa; font-family: Arial, sans-serif; }
            h1 { color: #00796b; text-align: center; }
            form { margin: 20px auto; width: 80%; max-width: 600px; padding: 20px; background-color: #ffffff; border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); }
            label { display: block; margin-bottom: 10px; font-weight: bold; color: #004d40; }
            input[type="text"], input[type="submit"] { width: 100%; padding: 12px; margin: 10px 0; }
            input[type="submit"] { background-color: #00796b; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #004d40; }
        </style>
        <h1>Rule Engine</h1>
        <form action="/create_rule" method="post">
            <label>Enter Rule String:</label>
            <input type="text" name="rule_string" placeholder="((age > 30 and department == 'Sales') or (age < 25 and department == 'Marketing'))" required>
            <input type="submit" value="Create Rule">
        </form>
        <form action="/evaluate_rule" method="post">
            <label>Enter JSON Data for Evaluation:</label>
            <input type="text" name="json_data" placeholder='{"age": 35, "department": "Sales", "salary": 60000, "experience": 6}' required>
            <input type="submit" value="Evaluate Rule">
        </form>
    ''')

# Route to create a rule
@app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    global global_rule_ast
    rule_string = request.form['rule_string']
    try:
        # Create the rule and store it globally
        global_rule_ast = create_rule(rule_string)
        return f"Rule Created: {global_rule_ast}", 200
    except Exception as e:
        return f"Error parsing rule: {str(e)}", 400

# Route to evaluate the rule
@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    global global_rule_ast
    if global_rule_ast is None:
        return "No rule created yet.", 400
    try:
        json_data = request.form['json_data']
        # Safely parse JSON data
        data = ast.literal_eval(json_data)
        # Evaluate the rule with the provided data
        result = evaluate_rule(global_rule_ast, data)
        return jsonify({"result": result}), 200
    except Exception as e:
        return f"Error evaluating rule: {str(e)}", 400

# Run Flask in a background thread
def run_flask_app():
    app.run(port=5000, debug=False)

thread = threading.Thread(target=run_flask_app)
thread.start()
