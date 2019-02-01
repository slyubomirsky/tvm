/*!
 *  Copyright (c) 2018 by Contributors
 * \file src/tvm/ir/adt.cc
 * \brief AST nodes for Relay algebraic data types (ADTs).
 */
#include <tvm/relay/type.h>
#include <tvm/relay/adt.h>

namespace tvm {
namespace relay {

PatternWildcard PatternWildcardNode::make() {
  NodePtr<PatternWildcardNode> n = make_node<PatternWildcardNode>();
  return PatternWildcard(n);
}

TVM_REGISTER_NODE_TYPE(PatternWildcardNode);

TVM_REGISTER_API("relay._make.PatternWildcard")
.set_body([](TVMArgs args, TVMRetValue* ret) {
    *ret = PatternWildcardNode::make();
  });

TVM_STATIC_IR_FUNCTOR_REGISTER(IRPrinter, vtable)
.set_dispatch<PatternWildcardNode>([](const PatternWildcardNode* node,
                                      tvm::IRPrinter* p) {
  p->stream << "PatternWildcardNode()";
});

PatternVar PatternVarNode::make(tvm::relay::Var var) {
  NodePtr<PatternVarNode> n = make_node<PatternVarNode>();
  n->var = std::move(var);
  return PatternVar(n);
}

TVM_REGISTER_NODE_TYPE(PatternVarNode);

TVM_REGISTER_API("relay._make.PatternVar")
.set_body([](TVMArgs args, TVMRetValue* ret) {
    *ret = PatternVarNode::make(args[0]);
  });

TVM_STATIC_IR_FUNCTOR_REGISTER(IRPrinter, vtable)
.set_dispatch<PatternVarNode>([](const PatternVarNode* node,
                                 tvm::IRPrinter* p) {
  p->stream << "PatternVarNode(" << node->var << ")";
});

PatternConstructor PatternConstructorNode::make(Constructor constructor,
                                                tvm::Array<Pattern> pat) {
  NodePtr<PatternConstructorNode> n = make_node<PatternConstructorNode>();
  n->constructor = std::move(constructor);
  n->pat = std::move(pat);
  return PatternConstructor(n);
}

TVM_REGISTER_NODE_TYPE(PatternConstructorNode);

TVM_REGISTER_API("relay._make.PatternConstructor")
.set_body([](TVMArgs args, TVMRetValue* ret) {
    *ret = PatternConstructorNode::make(args[0], args[1]);
  });

TVM_STATIC_IR_FUNCTOR_REGISTER(IRPrinter, vtable)
.set_dispatch<PatternConstructorNode>([](const PatternConstructorNode* node,
                                         tvm::IRPrinter* p) {
  p->stream << "PatternConstructorNode(" << node->constructor
            << ", " << node->pat << ")";
});

Constructor ConstructorNode::make(std::string name_hint,
                                  tvm::Array<Type> inp,
                                  GlobalTypeVar belong_to) {
  NodePtr<ConstructorNode> n = make_node<ConstructorNode>();
  n->name_hint = std::move(name_hint);
  n->inp = std::move(inp);
  n->belong_to = std::move(belong_to);
  return Constructor(n);
}

TVM_REGISTER_NODE_TYPE(ConstructorNode);

TVM_REGISTER_API("relay._make.Constructor")
.set_body([](TVMArgs args, TVMRetValue* ret) {
    *ret = ConstructorNode::make(args[0], args[1], args[2]);
  });

TVM_STATIC_IR_FUNCTOR_REGISTER(IRPrinter, vtable)
.set_dispatch<ConstructorNode>([](const ConstructorNode* node,
                                  tvm::IRPrinter* p) {
  p->stream << "ConstructorNode(" << node->name_hint << ", "
            << node->inp << ", " << node->belong_to << ")";
});

TypeData TypeDataNode::make(GlobalTypeVar header,
                            tvm::Array<TypeVar> tv,
                            tvm::Array<Constructor> constructors) {
  NodePtr<TypeDataNode> n = make_node<TypeDataNode>();
  n->header = std::move(header);
  n->tv = std::move(tv);
  n->constructors = std::move(constructors);
  return TypeData(n);
}

TVM_REGISTER_NODE_TYPE(TypeDataNode);

TVM_REGISTER_API("relay._make.TypeData")
.set_body([](TVMArgs args, TVMRetValue* ret) {
    *ret = TypeDataNode::make(args[0], args[1], args[2]);
  });

TVM_STATIC_IR_FUNCTOR_REGISTER(IRPrinter, vtable)
.set_dispatch<TypeDataNode>([](const TypeDataNode* node,
                               tvm::IRPrinter* p) {
  p->stream << "TypeDataNode(" << node->header << ", " << node->tv << ", "
            << node->constructors << ")";
});

Clause ClauseNode::make(Pattern lhs, Expr rhs) {
  NodePtr<ClauseNode> n = make_node<ClauseNode>();
  n->lhs = std::move(lhs);
  n->rhs = std::move(rhs);
  return Clause(n);
}

TVM_REGISTER_NODE_TYPE(ClauseNode);

TVM_REGISTER_API("relay._make.Clause")
.set_body([](TVMArgs args, TVMRetValue* ret) {
    *ret = ClauseNode::make(args[0], args[1]);
  });

TVM_STATIC_IR_FUNCTOR_REGISTER(IRPrinter, vtable)
.set_dispatch<ClauseNode>([](const ClauseNode* node,
                             tvm::IRPrinter* p) {
  p->stream << "ClauseNode(" << node->lhs << ", "
            << node->rhs << ")";
  });

Match MatchNode::make(Expr data, tvm::Array<Clause> pattern) {
  NodePtr<MatchNode> n = make_node<MatchNode>();
  n->data = std::move(data);
  n->pattern = std::move(pattern);
  return Match(n);
}

TVM_REGISTER_NODE_TYPE(MatchNode);

TVM_REGISTER_API("relay._make.Match")
.set_body([](TVMArgs args, TVMRetValue* ret) {
    *ret = MatchNode::make(args[0], args[1]);
  });

TVM_STATIC_IR_FUNCTOR_REGISTER(IRPrinter, vtable)
.set_dispatch<MatchNode>([](const MatchNode* node,
                            tvm::IRPrinter* p) {
  p->stream << "MatchNode(" << node->data << ", "
            << node->pattern << ")";
});

}  // namespace relay
}  // namespace tvm
